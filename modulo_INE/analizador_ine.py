import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


TABLAS_INE = {
    "demografia": 69301,
    "economia": 69303,
    "educacion": 69304
}

CARPETA_SALIDA = Path("salidas_ine_osint_final")
CARPETA_SALIDA.mkdir(exist_ok=True)

MAX_CLUSTERS = 8


def descargar_series_tabla(tabla_id):
    url = f"https://servicios.ine.es/wstempus/js/ES/SERIES_TABLA/{tabla_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()


def descargar_ultimo_valor(codigo_serie):
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{codigo_serie}?nult=1"
    r = requests.get(url, timeout=30)
    r.raise_for_status()

    data = r.json().get("Data", [])

    if not data:
        return None, None

    return data[0].get("Valor"), data[0].get("Anyo")


def limpiar_indicador(indicador):
    indicador = indicador.replace("Proporción de población entre 25-64 años con máximo nivel de educación ", "")
    indicador = indicador.replace("Proporción de ", "")
    indicador = indicador.replace(" sobre la población total (Porcentaje)", "")
    indicador = indicador.replace(" (Porcentaje)", "")
    indicador = indicador.replace(" (Euros)", "")
    indicador = indicador.replace("Total.", "")
    indicador = indicador.strip()
    return indicador


def indicador_util(indicador):
    texto = indicador.lower()

    prohibidos = [
        "guarderías",
        "mujeres",
        "hombres"
    ]

    for palabra in prohibidos:
        if palabra in texto:
            return False

    permitidos = [
        "tasa de desempleo",
        "ocupados entre 20-64",
        "tasa de actividad",
        "empleo en servicios",
        "empleo en industria",
        "renta neta media anual de los hogares",
        "renta neta media anual por habitante",
        "renta neta media anual por unidad de consumo",
        "isced 0, 1 ó 2",
        "isced 3 ó 4",
        "isced 5, 6, 7 ó 8",
        "población >=65 años",
        "edad mediana",
        "nacionales",
        "nacidos en el extranjero",
        "extranjeros"
    ]

    return any(p in texto for p in permitidos)


def extraer_ciudad_indicador(nombre_serie):
    partes = nombre_serie.split(". ")

    if len(partes) < 3:
        return None, None

    ciudad = partes[0].strip()
    indicador = partes[1].strip()

    if ciudad == "Total Nacional":
        return None, None

    return ciudad, indicador


def construir_dataset():
    registros = []

    for categoria, tabla_id in TABLAS_INE.items():
        print(f"\nConsultando tabla {tabla_id} ({categoria})...")

        series = descargar_series_tabla(tabla_id)
        print(f"Series encontradas: {len(series)}")

        for serie in series:
            nombre = serie["Nombre"]
            codigo = serie["COD"]

            ciudad, indicador = extraer_ciudad_indicador(nombre)

            if ciudad is None:
                continue

            if not indicador_util(indicador):
                continue

            valor, anyo = descargar_ultimo_valor(codigo)

            if valor is None:
                continue

            indicador_limpio = limpiar_indicador(indicador)

            registros.append({
                "ciudad": ciudad,
                "categoria": categoria,
                "indicador": indicador_limpio,
                "valor": valor,
                "anyo": anyo
            })

            print(f"OK: {ciudad} | {indicador_limpio} | {valor}")
            time.sleep(0.03)

    df_largo = pd.DataFrame(registros)

    df_largo.to_csv(
        CARPETA_SALIDA / "dataset_largo_ine_osint.csv",
        index=False,
        encoding="utf-8-sig"
    )

    matriz = df_largo.pivot_table(
        index="ciudad",
        columns="indicador",
        values="valor",
        aggfunc="first"
    ).reset_index()

    matriz.to_csv(
        CARPETA_SALIDA / "dataset_matriz_ine_osint.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return matriz, df_largo


def preparar_modelo(matriz):
    columnas = [c for c in matriz.columns if c != "ciudad"]

    matriz = matriz.copy()
    matriz[columnas] = matriz[columnas].replace([np.inf, -np.inf], np.nan)
    matriz[columnas] = matriz[columnas].apply(pd.to_numeric, errors="coerce")

    matriz = matriz.dropna()

    X = matriz[columnas]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return matriz, columnas, X_scaled


def seleccionar_mejor_k(X_scaled):
    resultados = []
    mejor_k = 2
    mejor_score = -1

    max_k = min(MAX_CLUSTERS, X_scaled.shape[0] - 1)

    for k in range(2, max_k + 1):
        modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
        etiquetas = modelo.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, etiquetas)

        resultados.append((k, score))

        if score > mejor_score:
            mejor_score = score
            mejor_k = k

    return mejor_k, resultados


def aplicar_clustering(matriz, columnas, X_scaled):
    mejor_k, scores = seleccionar_mejor_k(X_scaled)

    modelo = KMeans(n_clusters=mejor_k, random_state=42, n_init=10)
    matriz["cluster_ia"] = modelo.fit_predict(X_scaled)

    return matriz, mejor_k, scores


def generar_pca(matriz, X_scaled):
    pca = PCA(n_components=2)
    componentes = pca.fit_transform(X_scaled)

    matriz["pca_1"] = componentes[:, 0]
    matriz["pca_2"] = componentes[:, 1]

    ruta = CARPETA_SALIDA / "pca_clusters_ine_osint.png"

    plt.figure(figsize=(10, 7))
    plt.scatter(
        matriz["pca_1"],
        matriz["pca_2"],
        c=matriz["cluster_ia"],
        alpha=0.75
    )
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.title("Clustering OSINT territorial con datos INE")
    plt.colorbar(label="Cluster IA")
    plt.tight_layout()
    plt.savefig(ruta, dpi=300)
    plt.close()

    return ruta


def generar_perfiles(matriz, columnas):
    perfiles = matriz.groupby("cluster_ia")[columnas].mean()
    tamanos = matriz["cluster_ia"].value_counts().sort_index()
    return perfiles, tamanos


def interpretar_cluster(perfiles, cluster):
    perfil = perfiles.loc[cluster]
    global_media = perfiles.mean()

    altas = []
    bajas = []

    for col in perfiles.columns:
        if perfil[col] > global_media[col]:
            altas.append(col)
        elif perfil[col] < global_media[col]:
            bajas.append(col)

    texto = f"Cluster {cluster}: "

    if altas:
        texto += "valores superiores en " + ", ".join(altas[:5])
    else:
        texto += "sin valores claramente superiores"

    if bajas:
        texto += "; valores inferiores en " + ", ".join(bajas[:5])

    return texto


def generar_informe(matriz, columnas, mejor_k, scores, perfiles, tamanos, ruta_pca):
    ruta = CARPETA_SALIDA / "informe_osint_ine_final.md"

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Informe OSINT-INE: perfilado socioeconómico territorial mediante IA\n\n")

        f.write("## Objetivo\n\n")
        f.write(
            "Este prototipo consulta automáticamente la API del Instituto Nacional de Estadística "
            "y construye un dataset territorial con variables económicas, educativas y demográficas. "
            "Posteriormente aplica aprendizaje automático no supervisado para identificar agrupaciones "
            "de ciudades con características socioeconómicas similares.\n\n"
        )

        f.write("## Fuentes utilizadas\n\n")
        f.write("- INE OpenAPI / WSTempus\n")
        f.write("- Tabla 69301: Demografía\n")
        f.write("- Tabla 69303: Aspectos económicos\n")
        f.write("- Tabla 69304: Formación y educación\n\n")

        f.write("## Relación con OSINT\n\n")
        f.write(
            "El sistema utiliza fuentes abiertas institucionales para generar inteligencia territorial "
            "agregada. Este enfoque puede apoyar investigaciones OSINT al proporcionar contexto "
            "socioeconómico sobre territorios sin recurrir a información personal ni a vigilancia individual.\n\n"
        )

        f.write("## Variables utilizadas\n\n")
        for col in columnas:
            f.write(f"- {col}\n")

        f.write("\n## Metodología de IA\n\n")
        f.write(
            "Las variables se normalizan mediante StandardScaler y se aplica K-Means como técnica "
            "de aprendizaje automático no supervisado. El número de clusters se selecciona mediante "
            "Silhouette Score para evitar una elección arbitraria de K.\n\n"
        )

        f.write("## Selección automática de K\n\n")
        f.write(f"Número de clusters seleccionado: **{mejor_k}**\n\n")

        f.write("| K | Silhouette Score |\n")
        f.write("|---|------------------|\n")
        for k, score in scores:
            f.write(f"| {k} | {score:.4f} |\n")

        f.write("\n## Tamaño de los clusters\n\n")
        for cluster, tamano in tamanos.items():
            f.write(f"- Cluster {cluster}: {tamano} ciudades\n")

        f.write("\n## Perfil medio de los clusters\n\n")
        f.write(perfiles.round(3).to_markdown())
        f.write("\n\n")

        f.write("## Interpretación automática\n\n")
        for cluster in perfiles.index:
            f.write(f"- {interpretar_cluster(perfiles, cluster)}\n")

        f.write("\n## Visualización PCA\n\n")
        f.write(f"Gráfico generado: `{ruta_pca.name}`\n\n")

        f.write("## Limitaciones\n\n")
        f.write(
            "Los resultados no deben interpretarse como causalidad ni como clasificación definitiva. "
            "El clustering se emplea con finalidad exploratoria para detectar similitudes estructurales "
            "entre territorios y generar hipótesis de análisis en contextos OSINT.\n"
        )

    return ruta


def main():
    print("=== OSINT-INE SCRIPT IA FINAL ===")

    matriz, df_largo = construir_dataset()

    matriz_limpia, columnas, X_scaled = preparar_modelo(matriz)

    matriz_clusterizada, mejor_k, scores = aplicar_clustering(
        matriz_limpia,
        columnas,
        X_scaled
    )

    ruta_pca = generar_pca(matriz_clusterizada, X_scaled)

    perfiles, tamanos = generar_perfiles(matriz_clusterizada, columnas)

    matriz_clusterizada.to_csv(
        CARPETA_SALIDA / "dataset_clusterizado_ine_osint.csv",
        index=False,
        encoding="utf-8-sig"
    )

    perfiles.to_csv(
        CARPETA_SALIDA / "perfiles_clusters_ine_osint.csv",
        encoding="utf-8-sig"
    )

    ruta_informe = generar_informe(
        matriz_clusterizada,
        columnas,
        mejor_k,
        scores,
        perfiles,
        tamanos,
        ruta_pca
    )

    print("\nAnálisis completado.")
    print("Ciudades analizadas:", matriz_clusterizada.shape[0])
    print("Variables utilizadas:", len(columnas))
    print("Clusters seleccionados:", mejor_k)
    print("Carpeta de salida:", CARPETA_SALIDA)
    print("Informe:", ruta_informe)


if __name__ == "__main__":
    main()
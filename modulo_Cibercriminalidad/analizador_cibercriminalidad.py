import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


BASE_DIR = Path(__file__).resolve().parent

RUTA_DATOS = BASE_DIR / "datos" / "cibercriminalidad_provincias.csv"
CARPETA_SALIDA = BASE_DIR / "salidas"
CARPETA_SALIDA.mkdir(exist_ok=True)


ANIO_ANALISIS = 2024
MAX_CLUSTERS = 8

DELITOS_OBJETIVO = [
    "ACCESO ILEGAL INFORMÁTICO",
    "ACCESO ILEGAL A SISTEMAS INFORMÁTICOS",
    "ATAQUES A SISTEMAS INFORMÁTICOS",
    "ATAQUES A DATOS O PROGRAMAS INFORMÁTICOS"
]


def cargar_datos():
    df = pd.read_csv(RUTA_DATOS, sep=";", encoding="utf-8")
    df.columns = df.columns.str.strip()

    print("Columnas detectadas:", list(df.columns))
    print("Filas cargadas:", len(df))

    return df


def preparar_dataset(df):
    df = df.rename(columns={
        "Provincias": "provincia",
        "Tipología penal": "tipologia",
        "periodo": "anio",
        "Total": "total"
    })

    df["tipologia"] = df["tipologia"].astype(str).str.strip().str.upper()
    df["provincia"] = df["provincia"].astype(str).str.strip()
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df["total"] = (
        df["total"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["total"] = pd.to_numeric(df["total"], errors="coerce")

    df = df[df["anio"] == ANIO_ANALISIS]
    df = df[df["tipologia"].isin(DELITOS_OBJETIVO)]

    print("Filas tras filtrado:", len(df))
    print("Provincias:", df["provincia"].nunique())
    print("Tipologías:", df["tipologia"].nunique())

    matriz = df.pivot_table(
        index="provincia",
        columns="tipologia",
        values="total",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    matriz["TOTAL_ATAQUES_ACCESOS"] = matriz[
        [col for col in matriz.columns if col != "provincia"]
    ].sum(axis=1)

    matriz.to_csv(
        CARPETA_SALIDA / "dataset_cibercriminalidad_matriz.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return matriz


def seleccionar_mejor_k(X):
    mejor_k = 2
    mejor_score = -1
    resultados = []

    max_k = min(MAX_CLUSTERS, X.shape[0] - 1)

    for k in range(2, max_k + 1):
        modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
        etiquetas = modelo.fit_predict(X)
        score = silhouette_score(X, etiquetas)

        resultados.append((k, score))

        if score > mejor_score:
            mejor_score = score
            mejor_k = k

    return mejor_k, resultados


def aplicar_ia(matriz):
    columnas = [c for c in matriz.columns if c != "provincia"]

    X = matriz[columnas].replace([np.inf, -np.inf], np.nan).fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    mejor_k, scores = seleccionar_mejor_k(X_scaled)

    modelo = KMeans(n_clusters=mejor_k, random_state=42, n_init=10)
    matriz["cluster_ia"] = modelo.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    componentes = pca.fit_transform(X_scaled)

    matriz["pca_1"] = componentes[:, 0]
    matriz["pca_2"] = componentes[:, 1]

    return matriz, columnas, mejor_k, scores, X_scaled


def generar_grafico(matriz):
    ruta = CARPETA_SALIDA / "pca_cibercriminalidad.png"

    plt.figure(figsize=(10, 7))
    plt.scatter(
        matriz["pca_1"],
        matriz["pca_2"],
        c=matriz["cluster_ia"],
        alpha=0.75
    )
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")
    plt.title("Clustering de cibercriminalidad por provincias")
    plt.colorbar(label="Cluster IA")
    plt.tight_layout()
    plt.savefig(ruta, dpi=300)
    plt.close()

    return ruta


def generar_informe(matriz, columnas, mejor_k, scores, ruta_grafico):
    perfiles = matriz.groupby("cluster_ia")[columnas].mean()
    tamanos = matriz["cluster_ia"].value_counts().sort_index()

    ruta = CARPETA_SALIDA / "informe_cibercriminalidad.md"

    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Informe de Cibercriminalidad\n\n")

        f.write("## Objetivo\n\n")
        f.write(
            "Este módulo analiza estadísticas oficiales de cibercriminalidad "
            "procedentes del Portal Estadístico de Criminalidad del Ministerio del Interior. "
            "El objetivo es construir un dataset estructurado por provincias y aplicar "
            "técnicas de aprendizaje automático no supervisado para identificar patrones "
            "en delitos relacionados con accesos y ataques informáticos.\n\n"
        )

        f.write("## Variables utilizadas\n\n")
        for col in columnas:
            f.write(f"- {col}\n")

        f.write("\n## Selección automática de K\n\n")
        f.write(f"Número de clusters seleccionado: **{mejor_k}**\n\n")

        f.write("| K | Silhouette Score |\n")
        f.write("|---|------------------|\n")
        for k, score in scores:
            f.write(f"| {k} | {score:.4f} |\n")

        f.write("\n## Tamaño de los clusters\n\n")
        for cluster, tamano in tamanos.items():
            f.write(f"- Cluster {cluster}: {tamano} provincias\n")

        f.write("\n## Perfil medio de los clusters\n\n")
        f.write(perfiles.round(3).to_markdown())
        f.write("\n\n")

        f.write("## Visualización PCA\n\n")
        f.write(f"Gráfico generado: `{ruta_grafico.name}`\n\n")

        f.write("## Aplicación OSINT\n\n")
        f.write(
            "El análisis permite identificar provincias con patrones similares de "
            "cibercriminalidad, proporcionando una capa de contexto útil para investigaciones "
            "OSINT centradas en amenazas digitales y distribución geográfica de incidentes.\n"
        )

    return ruta


def main():
    print("=== MÓDULO CIBERCRIMINALIDAD ===")

    df = cargar_datos()
    matriz = preparar_dataset(df)

    matriz_clusterizada, columnas, mejor_k, scores, X_scaled = aplicar_ia(matriz)

    ruta_grafico = generar_grafico(matriz_clusterizada)

    matriz_clusterizada.to_csv(
        CARPETA_SALIDA / "dataset_clusterizado_cibercriminalidad.csv",
        index=False,
        encoding="utf-8-sig"
    )

    ruta_informe = generar_informe(
        matriz_clusterizada,
        columnas,
        mejor_k,
        scores,
        ruta_grafico
    )

    print("\nAnálisis completado.")
    print("Provincias analizadas:", matriz_clusterizada.shape[0])
    print("Variables utilizadas:", len(columnas))
    print("Clusters seleccionados:", mejor_k)
    print("Informe:", ruta_informe)


if __name__ == "__main__":
    main()
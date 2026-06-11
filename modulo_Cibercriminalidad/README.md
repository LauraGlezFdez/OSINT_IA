# Módulo Cibercriminalidad

## Descripción

Módulo orientado al análisis automatizado de estadísticas oficiales de criminalidad y cibercriminalidad procedentes de fuentes abiertas institucionales.

El objetivo es construir conjuntos de datos que permitan estudiar patrones geográficos y temporales relacionados con la ciberdelincuencia, así como su posible relación con indicadores socioeconómicos procedentes de otras fuentes oficiales.

---

## Fuente de datos

Portal Estadístico de Criminalidad.

Ministerio del Interior.

https://estadisticasdecriminalidad.ses.mir.es

---
## Ejecución del módulo de cibercriminalidad

El sistema requiere como entrada el conjunto de datos oficial empleado para el análisis de la cibercriminalidad provincial.

### Opción 1: Utilizar el fichero incluido en el repositorio

El repositorio incorpora el fichero `cibercriminalidad_provincias.csv`, por lo que el análisis puede ejecutarse directamente mediante:

```bash
pip install -r requirements.txt
python analizador_cibercriminalidad.py
```

### Opción 2: Descargar nuevamente los datos desde la fuente oficial

Alternativamente, el usuario puede obtener la información actualizada desde el Portal Estadístico de Criminalidad del Ministerio del Interior. Una vez descargado el fichero correspondiente, deberá guardarse con el nombre `cibercriminalidad_provincias.csv` en la misma carpeta que el script `analizador_cibercriminalidad.py`.

Posteriormente, la ejecución se realiza mediante:

```bash
pip install -r requirements.txt
python analizador_cibercriminalidad.py
```

En ambos casos, el sistema procesará automáticamente los datos, aplicará las técnicas de aprendizaje automático definidas y generará los resultados correspondientes.

Con el fin de garantizar la reproducibilidad del análisis, el conjunto de datos utilizado durante el desarrollo se incluye en el repositorio. No obstante, el sistema permite igualmente emplear versiones actualizadas del dataset obtenidas directamente desde la fuente oficial.
---

## Objetivos

- Obtención automatizada de estadísticas de cibercriminalidad.
- Construcción de datasets estructurados.
- Análisis exploratorio.
- Aplicación de técnicas de aprendizaje automático no supervisado (K-Means y PCA).
- Generación automática de informes y visualizaciones para el análisis de resultados.
---


## NOTA: Todo este proyecto ha sido desarrollado como parte del Trabajo de Fin de Estudio, en el Grado en Ingeniería Informática de UNIR.

# Sistema Inteligencia

## Descripción

Sistema experimental orientado a la obtención, integración, procesamiento y análisis automatizado de información procedente de fuentes abiertas institucionales mediante técnicas de Ciencia de Datos, Aprendizaje Automático e Inteligencia Artificial.

El proyecto explora la aplicación de metodologías OSINT (Open Source Intelligence) sobre conjuntos de datos públicos procedentes de organismos oficiales españoles, permitiendo la automatización de tareas de tratamiento de datos, la identificación de patrones y la generación de análisis a partir de información de acceso abierto.

Para ello, se implementan procesos de limpieza, transformación, visualización y agrupamiento de datos mediante algoritmos de aprendizaje no supervisado, facilitando la detección de relaciones y tendencias presentes en los conjuntos de datos analizados.

Este desarrollo forma parte de una investigación académica sobre la integración de técnicas de Inteligencia Artificial en entornos OSINT y su aplicación al análisis de información procedente de fuentes abiertas.

---

## Arquitectura General

EEl sistema se organiza en módulos independientes orientados al procesamiento y análisis de información procedente de diferentes fuentes abiertas institucionales.

### Módulo INE

Módulo destinado a la obtención y análisis automatizado de indicadores demográficos, económicos y educativos procedentes del Instituto Nacional de Estadística (INE).

Funcionalidades principales:

- Consulta automática de la API oficial del INE.
- Descubrimiento de series estadísticas relevantes.
- Construcción de conjuntos de datos multivariables.
- Limpieza y normalización de datos.
- Agrupamiento mediante algoritmos de aprendizaje no supervisado.
- Determinación del número de grupos para el análisis.
- Generación de visualizaciones mediante PCA.
- Elaboración automática de informes analíticos.

### Módulo de Cibercriminalidad

Módulo orientado al análisis de estadísticas oficiales de criminalidad y cibercriminalidad procedentes de organismos públicos.

---

## Tecnologías empleadas

- Python
- Pandas
- NumPy
- Matplotlib
- Requests
- APIs REST
- Scikit-Learn
- StandardScaler
- K-Means
- Silhouette Score
- Análisis de Componentes Principales (PCA)

---

## Objetivos de investigación

1. Automatizar la obtención de información procedente de fuentes abiertaS.
2. Evaluar la aplicación de técnicas de aprendizaje automático al análisis exploratorio de datos públicos.
3. Facilitar el tratamiento y análisis automatizado de conjuntos de datos abiertos.
4. Identificar patrones ocultos mediante técnicas de aprendizaje automático no supervisado.
5. Explorar la integración de técnicas de Inteligencia Artificial en procesos de análisis de información procedente de fuentes abiertas.

---


# Sistema Inteligencia

## Descripción

Sistema experimental para la obtención, integración y análisis automatizado de información procedente de fuentes abiertas institucionales mediante técnicas de Ciencia de Datos e Inteligencia Artificial.

El proyecto tiene como objetivo explorar la aplicación de metodologías OSINT (Open Source Intelligence) sobre fuentes oficiales españolas, permitiendo la construcción de perfiles analíticos a partir de datos públicos y la identificación automática de patrones mediante algoritmos de aprendizaje no supervisado.

Este desarrollo forma parte de una investigación sobre la aplicación de técnicas de Inteligencia Artificial al análisis de información obtenida desde fuentes abiertas.

---

## Arquitectura General

El sistema se organiza en módulos independientes especializados en distintas fuentes de información.

### Módulo INE

Obtención y análisis automatizado de indicadores demográficos, económicos y educativos procedentes del Instituto Nacional de Estadística.

Funcionalidades principales:

- Consulta automática de la API oficial del INE.
- Descubrimiento de series estadísticas relevantes.
- Construcción de conjuntos de datos multivariables.
- Normalización de variables.
- Clustering mediante algoritmos de aprendizaje no supervisado.
- Selección automática del número óptimo de grupos.
- Generación de visualizaciones mediante PCA.
- Elaboración automática de informes analíticos.

### Módulo de Cibercriminalidad

Módulo orientado al análisis de estadísticas oficiales de criminalidad y cibercriminalidad procedentes de organismos públicos.

Estado actual: En desarrollo.

---

## Tecnologías empleadas

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Requests
- APIs REST
- Técnicas de Machine Learning No Supervisado

---

## Objetivos de investigación

1. Automatizar la obtención de información desde fuentes abiertas oficiales.
2. Evaluar la utilidad de técnicas de IA para el análisis exploratorio de datos públicos.
3. Generar perfiles analíticos de forma automática.
4. Estudiar la integración de múltiples fuentes OSINT en un entorno unificado de análisis.

---


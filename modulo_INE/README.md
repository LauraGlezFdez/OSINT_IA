## NOTA: Este módulo forma parte del código fuente desarrollado para el Trabajo Fin de Estudios del Grado en Ingeniería Informática de la Universidad Internacional de La Rioja (UNIR).

# Módulo INE

## Descripción

Módulo encargado de la obtención y análisis automatizado de información estadística procedente de la API oficial del Instituto Nacional de Estadística (INE).

Su objetivo es construir conjuntos de datos a partir de indicadores demográficos, económicos y educativos, permitiendo posteriormente la aplicación de técnicas de análisis exploratorio y aprendizaje automático.

Este módulo constituye un caso práctico de aplicación de técnicas de aprendizaje automático no supervisado sobre una fuente OSINT institucional accesible mediante API pública.

---

## Fuente de datos

Instituto Nacional de Estadística (INE)

Servicio utilizado:

[https://servicios.ine.es/wstempus/js/ES/](https://www.ine.es/OpenAPI/index.html)

---

## Funcionalidades implementadas

- Consulta automática de la API del INE.
- Descubrimiento y explotación de series estadísticas.
- Construcción automática de datasets estructurados.
- Integración de indicadores socioeconómicos.
- Normalización y preparación de datos.
- Clustering mediante algoritmos de aprendizaje no supervisado.
- Selección automática del número de grupos.
- Reducción de dimensionalidad y visualización de resultados mediante PCA.
- Elaboración automática de informes.

---

## Variables utilizadas

El sistema trabaja con indicadores pertenecientes a tres grandes categorías:

### Economía

- Tasa de desempleo.
- Tasa de actividad.
- Ocupación.
- Empleo industrial.
- Empleo en servicios.
- Renta media de los hogares.
- Renta media por habitante.
- Renta media por unidad de consumo.

### Educación

- Nivel educativo ISCED 0-2.
- Nivel educativo ISCED 3-4.
- Nivel educativo ISCED 5-8.

### Demografía

- Edad mediana de la población.
- Población mayor de 65 años.
- Nacionalidad.
- Población nacida en el extranjero.
- Población extranjera.

---

## Resultados actuales

- 111 ciudades analizadas.
- 17 variables integradas en el modelo.
- Identificación automática de 5 clústeres mediante K-Means.
- Generación automática de perfiles de clústeres.
- Visualización de resultados mediante PCA.
- Generación automática de informes en formato Markdown.

---


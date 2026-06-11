# Módulo INE

## Descripción

Módulo encargado de la obtención y análisis automatizado de información estadística procedente de la API oficial del Instituto Nacional de Estadística (INE).

Su objetivo es construir conjuntos de datos a partir de indicadores demográficos, económicos y educativos, permitiendo posteriormente la aplicación de técnicas de análisis exploratorio y aprendizaje automático.

---

## Fuente de datos

Instituto Nacional de Estadística (INE)

Servicio utilizado:

https://servicios.ine.es/wstempus/js/ES/

---

## Funcionalidades implementadas

- Consulta automática de la API del INE.
- Descubrimiento y explotación de series estadísticas.
- Construcción de datasets estructurados.
- Integración de indicadores socioeconómicos.
- Normalización y preparación de datos.
- Clustering mediante algoritmos de aprendizaje no supervisado.
- Selección automática del número de grupos.
- Generación de visualizaciones mediante PCA.
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

- Más de 100 ciudades analizadas.
- 17 variables integradas en el modelo.
- Clustering automático mediante K-Means.
- Generación de perfiles diferenciados.
- Visualización PCA.
- Informe automático en formato Markdown.

---


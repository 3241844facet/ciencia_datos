# Informe Técnico Final: Pipeline Analítico del Minimercado

**Autores:** David Reese & Diana Moré  
**Fecha:** Noviembre 2026  

---

## 1. Arquitectura del Pipeline

El proyecto implementa una arquitectura basada en el **Modern Data Stack (MDS)**:

1. **Capa de Generación:** Script Python (`generar_datos.py`) con semilla fija (`seed=42`) para reproducibilidad.
2. **Capa de Ingesta:** Librería `dlt` para extracción de archivos CSV y carga en DuckDB con estrategia `replace` (garantizando idempotencia).
3. **Capa de Almacenamiento:** DuckDB (`data.duckdb`) como motor analítico *in-process*.
4. **Capa de Transformación:** `dbt` estructurado en Staging, Intermediate y Marts.
5. **Capa de Orquestación y QA:** Dagster y Pytest garantizando ejecución fluida y control de calidad.

---

## 2. Decisión de Modelado Analítico y Calidad

Se adoptó una arquitectura en tres capas dentro de `dbt`:
* **Staging:** Limpieza, renombrado estandarizado y casteo explícito de tipos de datos.
* **Intermediate:** Consolidación de inventarios calculando netos de entradas y salidas de stock.
* **Marts:** Modelado dimensional enfocado en el negocio:
  * `mart_ventas_diarias`: Métricas agregadas y variabilidad diaria.
  * `mart_rentabilidad_productos`: Ganancia bruta y **Clasificación ABC** (regla 70/20/10).
  * `mart_rotacion_inventario`: Cobertura estimada de stock.
  * `mart_desempeno_vendedores`: Métricas de venta por vendedor.

---

## 3. Principales Hallazgos Estadísticos y Comerciales

* **Ventas Totales:** Se observó un flujo de ventas uniforme de 90 días con picos asociados a promociones con descuento.
* **Clasificación ABC:** El 70% de los ingresos se concentran en aproximadamente 5 productos clave (Categoría A), lo que respalda una estrategia de inventario focalizada.
* **Fidelización y Fuerza de Ventas:** Los vendedores mostraron distribución uniforme entre sucursales, con un rendimiento promedio equilibrado.

---

## 4. Limitaciones y Oportunidades de Mejora

* **Simulación de Demanda:** La variabilidad estacional es simplificada; se puede integrar elasticidad precio-demanda en futuras iteraciones.
* **Ingesta incremental:** Implementar `append` o `merge` incremental en `dlt` para entornos con grandes volúmenes de datos.
# Informe de unidad -- plantilla

Informe técnico acotado para el cierre de cada unidad

---

## Unidad: U2: Mi primer pipeline de datos con dlt y DuckDB

**Nombre:** David Helmut Reese Molinas

**Usuario GitHub:** 3241844facet

**Fecha:** 25 de Octubre de 2026

**Tag de cierre:** `u2-completa`

---

### Qué se hizo

En esta segunda unidad construí un pipeline de extracción y carga (EL) automatizado en Python utilizando la librería
`dlt` para consumir datos paginados desde una API pública REST (Rick and Morty API) y persistirlos directamente en un
motor analítico `DuckDB`.

#### Entorno
Trabajé sobre el entorno configurado en la unidad anterior, asegurando la instalación de las dependencias `dlt` y
`duckdb` mediante el gestor `uv`. Verifiqué la disponibilidad de las herramientas ejecutando los scripts del entorno.

#### Flujo de Git
Creé la rama de trabajo `u2/3241844facet` e introduje los archivos dentro de la carpeta
`u2-pipeline/entregas/3241844facet/`. Realicé más de tres commits pequeños y explicativos según las buenas prácticas de
desarrollo y abrí el Pull Request correspondiente hacia el repositorio original.

---

### Una decisión de diseño, explicada

Elegí utilizar el decorador `@dlt.resource` configurado con la disposición `write_disposition="replace"` para la
gestión del almacenamiento de la tabla `personajes`.

Al consumir una API externa que entrega la lista completa de la entidad, implementar una estrategia de reemplazo
garantiza la idempotencia del pipeline de datos. Si el proceso de ingesta se ejecuta múltiples veces
consecutivas (por ejemplo, en un entorno de integración continua o en ejecuciones programadas), `dlt` recrea la tabla de
forma limpia sin duplicar registros ni requerir lógica compleja de deduplicación manual.

Adicionalmente, diseñé la extracción utilizando un generador `while` con `yield` para consumir la paginación de la API
por lotes de manera eficiente, evitando sobrecargar la memoria RAM al procesar volúmenes crecientes de datos.

---

### Un problema que apareció

Durante las pruebas iniciales con `dlt`, el esquema automático infirió tipos de datos dinámicos basados en la primera
página devuelta por la API. Sin embargo, al procesar páginas subsecuentes, algunos campos JSON anidados (como la
ubicación u origen del personaje) presentaban estructuras variables.

Esto generaba advertencias en la evolución del esquema relacional y la creación no deseada de tablas secundarias
anidadas no planificadas en DuckDB.

Lo resolví revisando el comportamiento de normalización automática de `dlt`. Al no forzar esquemas rígidos antes de la
ingesta, `dlt` logró aplanar los objetos JSON anidados en columnas compuestas (`origin__name`, `location__name`).
Comprobé el resultado abriendo `data.duckdb` desde el script `verificar_datos.py`, constatando que la estructura de la
tabla final era limpia, coherente y fácil de consultar en SQL estándar.

---

### Reflexión y ayudas externas

#### Reflexión
Trabajar con `dlt` y `DuckDB` simplifica drásticamente la construcción de pipelines de datos. `dlt` elimina la
necesidad de escribir código repetitivo para el manejo de esquemas o conectores, mientras que `DuckDB` ofrece una
persistencia local sin requerir la administración de servidores de bases de datos pesados.

#### Ayudas externas
Para completar la tarea utilicé la documentación oficial de dlt sobre recursos paginados
(https://dlthub.com/docs/general-usage/resource) y la documentación de DuckDB Python API
(https://duckdb.org/docs/api/python/overview).

Asimismo, utilicé la asistencia de Gemini para estructurar las pruebas unitarias con mocks (`unittest.mock`) y
garantizar el formato adecuado del informe dentro del rango de palabras requerido.

---

### Qué harías distinto con más tiempo

Con más tiempo, implementaría carga incremental (`incremental`) basada en marcas de tiempo para evitar re-descargar la
totalidad de los registros en cada corrida, y agregaría validaciones de calidad de datos con `great_expectations` o
contratos de datos de `dlt`.
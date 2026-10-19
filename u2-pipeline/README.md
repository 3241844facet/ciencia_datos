# Tarea U2: Mi primer pipeline de datos con dlt y DuckDB

Construirás tu primer pipeline de datos reproducible utilizando dlt para extraer información desde una API pública, validar la estructura y cargar los datos de manera persistente en DuckDB, consultándolos posteriormente.

## Qué se requiere realizar

1. Configurar el entorno, utilizando de base el repositorio fork propio.

2. Crear el script del pipeline. En tu carpeta de entrega, crea un archivo **pipeline.py** que utilice la librería **dlt** para conectar a una API pública (por ejemplo, la API gratuita de JSONPlaceholder o Rick and Morty API).

3. Definir el recurso y la carga. Extrae los datos de la API, configuralos mediante un recurso de dlt y cárgalos en una base de datos local llamada **data.duckdb** bajo un esquema y tabla limpios.

4. Validar con una consulta. Crea un segundo script o una función de verificación **verificar_datos.py** que abra la base de datos DuckDB mediante Python, ejecute una consulta SQL básica (por ejemplo, conteo de registros o filtrado) y muestre los resultados por consola.

5. Escribir pruebas. En la misma carpeta, crea **test_pipeline.py** con al menos dos pruebas utilizando pytest (una para validar la correcta conexión/estructura del recurso dlt y otra para un caso borde, como manejar una respuesta vacía o un error de conexión simulado).

6. Trabaja con Git. Crea la rama u2/<tu-usuario> y haz al menos tres commits pequeños y claros.

7. Abre el Pull Request. Envía tu PR al repositorio del curso tocando únicamente tu carpeta de entrega.

8. Escribe el informe. Agrega informe.md (500 a 700 palabras) explicando las decisiones de diseño, cómo lidiaste con el esquema automático de dlt y qué te pareció trabajar con DuckDB.

## Qué contiene tu carpeta de entrega

```
u2-pipeline/entregas/<tu-usuario>/
├── pipeline.py         # Código del pipeline con dlt
├── verificar_datos.py  # Script de consulta a DuckDB
├── test_pipeline.py    # Pruebas con pytest
└── informe.md          # Informe técnico (500 a 700 palabras)
```

## Cómo revisar tu trabajo antes de entregar

Desde la raíz del repositorio, con tu usuario en lugar de `<usuario>`:

```bash
# Validar estilo y formato con ruff
ruff check u2-pipeline/entregas/<usuario>
ruff format --check u2-pipeline/entregas/<usuario>

# Ejecutar el pipeline para generar la base DuckDB
python u2-pipeline/entregas/<usuario>/pipeline.py

# Verificar los datos cargados mediante DuckDB
python u2-pipeline/entregas/<usuario>/verificar_datos.py

# Ejecutar las pruebas unitarias
pytest u2-pipeline/entregas/<usuario>

```

## Criterios de aceptación

- El script pipeline.py se ejecuta sin errores y genera correctamente el archivo data.duckdb.
- ruff check no reporta errores de linting en tu carpeta.
- pytest pasa satisfactoriamente con al menos dos pruebas implementadas.
- El PR cuenta con tres o más commits y modifica exclusivamente la carpeta correspondiente al estudiante (entregas/<tu-usuario>/).

## Puntos de evaluación (100 puntos)

- Funcionamiento del Pipeline y Persistencia: Extracción correcta de la API y almacenamiento funcional en DuckDB (35 puntos).
- Flujo de Git: Rama correcta, mensajes de commit descriptivos y PR bien documentado (25 puntos).
- Calidad del Código y Pruebas: Código limpio validado con ruff y pruebas robustas con pytest (20 puntos).
- Informe Técnico: Claridad conceptual, evidencias de ejecución y reflexión crítica sobre el uso de dlt y DuckDB (20 puntos).

## Reglas

- Trabajo individual. Puedes consultar documentación, foros y herramientas de IA:
  decláralo en el informe y asegúrate de poder explicar cada línea que entregas.
- No subas claves ni datos personales.
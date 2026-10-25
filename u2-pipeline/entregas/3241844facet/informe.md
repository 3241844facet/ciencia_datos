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
`dlt` para consumir datos paginados desde la API pública PokeAPI (`https://pokeapi.co/api/v2/pokemon`), enriquecerlos
con metadatos detallados de cada entidad (tipos, habilidades y movimientos principales) e insertarlos en el motor
analítico `DuckDB`.

#### Entorno
Trabajé sobre el entorno configurado en el Dev Container del repositorio. Verifiqué la instalación de las
dependencias `dlt`, `duckdb` y `requests`, asegurando que los comandos de prueba y linter ejecutaran correctamente.

#### Flujo de Git
Creé la rama de trabajo `u2/3241844facet` e introduje los archivos dentro de la carpeta
`u2-pipeline/entregas/3241844facet/`. Realicé tres commits pequeños y explicativos según las buenas prácticas de
desarrollo y abrí el Pull Request correspondiente en mi fork hacia mi rama `main`.

---

### Una decisión de diseño, explicada

Elegí estructurar un pipeline de dos niveles dentro del recurso `pokemon` que serializa los atributos anidados mediante
`json.dumps()`.

Inicialmente, al enviar listas de Python dentro del diccionario (como `tipos: ['grass']`), el motor de normalización de
`dlt` intentaba crear tablas relacionales secundarias conectadas por claves foráneas (`pokemon__tipos`). Para
mantener un esquema plano de una sola tabla relacional en DuckDB, serialicé los arreglos a cadenas en formato JSON.
Esto permite consultar los metadatos en una única tabla `raw_pokeapi.pokemon` sin requerir JOINs complejos.

Adicionalmente, implementé la eliminación previa del archivo `data.duckdb` en `main()` usando `Path.unlink()` para
garantizar la reconstrucción desde cero en cada ejecución, e incorporé pausas de *cooldown* con `time.sleep` para
evitar el bloqueo o estrangulamiento de la IP por solicitudes consecutivas (*rate limiting*).

---

### Un problema que apareció

Durante la ejecución y pruebas del pipeline se identificaron dos problemas principales.

En primer lugar, realizar múltiples peticiones consecutivas por cada Pokémon a la API pública podía causar un bloqueo
temporal o error HTTP 429 por saturación de tráfico. Lo solucioné implementando pausas cortas de 0.1s por detalle y
0.5s entre páginas, asegurando un consumo eficiente y respetuoso del servidor.

En segundo lugar, la integración de metadatos enriquecidos requirió adaptar las pruebas unitarias en Pytest. Al
hacer peticiones anidadas, se implementó un mockeo multinivel con `side_effect` en `requests.get` para simular tanto
la lista paginada como los JSONs individuales. Asimismo, se gestionó la abstracción de `dlt`, que aplana los
generadores con listas y envuelve las fallas de red dentro de su excepción interna `ResourceExtractionError`.

Lo resolví manteniendo una suite de 6 pruebas unitarias que verifican la serialización JSON de atributos, la
paginación múltiple, el manejo de respuestas vacías, errores de red HTTP 500 y las pausas con `mock_sleep`.

---

### Reflexión y ayudas externas

#### Reflexión
Trabajar con `dlt` y `DuckDB` simplifica drásticamente la construcción de pipelines de datos. `dlt` elimina la
necesidad de escribir código repetitivo para el manejo de esquemas o conectores, mientras que `DuckDB` ofrece una
persistencia local sin requerir la administración de servidores de bases de datos pesados.

#### Ayudas externas
Para completar la tarea utilicé la documentación oficial de dlt sobre recursos paginados y excepciones
(https://dlthub.com/docs/) y la guía oficial de Pytest para el uso de mocks (https://docs.pytest.org/en/stable/).

Asimismo, utilicé la asistencia interactiva de Gemini para depurar la creación no deseada de tablas secundarias por
normalización en `dlt`, adaptar los mocks de Pytest al esquema serializado con `json.dumps()` y redactar el informe.

---

### Qué harías distinto con más tiempo

Con más tiempo, implementaría carga incremental (`incremental`) basada en marcas de tiempo para evitar re-descargar la
totalidad de los registros en cada corrida, y agregaría validaciones de calidad de datos con contratos de datos de
`dlt`.
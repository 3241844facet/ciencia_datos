# Pipeline Analítico de Minimercado — Modern Data Stack
Proyecto integrador que implementa un pipeline ETL/ELT analítico end-to-end reproducible.

## Integrantes del Equipo
* **David Reese**: Data Engineer (Generación sintética, Ingesta idempotente con dlt, DuckDB).
* **Diana Moré**: Analytics Engineer & QA (Modelado dbt, Orquestación con Dagster, Pytest, Informe).

---
## Requisitos Previos
* Python 3.10 o superior
* Git

---
## Guía de Instalación y Ejecución Paso a Paso
### 1. Entorno e Instalación de Dependencias
```bash
python -m venv venv
source venv/bin/activate
pip install "dlt[duckdb]" dbt-duckdb dagster pytest pandas
```

2. Generación de Datos Sintéticos
```Bash
python generar_datos.py
```

3. Ingesta a DuckDB con dlt
```Bash
python pipeline.py
```

4. Transformaciones y Pruebas con dbt
```Bash
cd dbt_project
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..
```

5. Orquestación Automatizada con Dagster
```Bash
dagster dev -f orchestration/definitions.py
```

6. Ejecución del Suite de Pruebas Automatizadas
```Bash
pytest test_pipeline.py -v
```
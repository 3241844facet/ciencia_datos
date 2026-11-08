import subprocess
from dagster import Definitions, asset


@asset
def generar_datos_asset():
    """Ejecuta el script de generación de datos sintéticos."""
    from generar_datos import generar_datos_minimercado

    generar_datos_minimercado()


@asset(deps=[generar_datos_asset])
def ingesta_dlt_asset():
    """Carga los CSVs hacia DuckDB usando dlt."""
    from pipeline import run_pipeline

    run_pipeline()


@asset(deps=[ingesta_dlt_asset])
def dbt_transformations_asset():
    """Ejecuta dbt run y dbt test en la carpeta dbt_project."""
    subprocess.run(["dbt", "run"], cwd="dbt_project", check=True)
    subprocess.run(["dbt", "test"], cwd="dbt_project", check=True)


@asset(deps=[dbt_transformations_asset])
def reporte_calidad_asset():
    """Validación final post-transformación."""
    import duckdb

    con = duckdb.connect("data.duckdb")
    count = con.execute(
        "SELECT COUNT(*) FROM main.mart_rentabilidad_productos"
    ).fetchone()[0]
    con.close()
    assert count > 0, "Error QA: El Mart de rentabilidad no contiene datos."


defs = Definitions(
    assets=[
        generar_datos_asset,
        ingesta_dlt_asset,
        dbt_transformations_asset,
        reporte_calidad_asset,
    ]
)
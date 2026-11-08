import dlt
import pandas as pd


def cargar_archivos_csv():
    """Generador que cede cada dataset CSV como recurso dlt."""
    tablas = [
        "productos",
        "vendedores",
        "compras",
        "ventas",
        "movimientos_stock",
    ]
    for tabla in tablas:
        df = pd.read_csv(f"data/{tabla}.csv")
        yield dlt.resource(
            df,
            name=tabla,
            write_disposition="replace",  # Idempotencia al reejecutar
        )


def run_pipeline():
    """Carga de archivos CSV hacia la base de datos DuckDB."""
    pipeline = dlt.pipeline(
        pipeline_name="minimercado_ingestion",
        destination="duckdb",
        dataset_name="main",
    )
    load_info = pipeline.run(cargar_archivos_csv(), credentials="data.duckdb")
    print(load_info)


if __name__ == "__main__":
    run_pipeline()
    print("✅ Ingesta con dlt completada con éxito en 'data.duckdb'.")
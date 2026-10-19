""" Corre el pipeline de ingesta completo: CSV -> DuckDB. """

from __future__ import annotations

import logging

import dlt

from source import car_sales_source

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def construir_pipeline() -> dlt.Pipeline:
    return dlt.pipeline(
        pipeline_name="car_sales",
        destination="duckdb",
        dataset_name="raw_carsales",
    )


def main() -> None:
    pipeline = construir_pipeline()
    info = pipeline.run(car_sales_source())
    print(info)


if __name__ == "__main__":
    main()

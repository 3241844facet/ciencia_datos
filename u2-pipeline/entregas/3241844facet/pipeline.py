"""Pipeline de ingesta utilizando dlt y DuckDB desde una API pública."""

from __future__ import annotations

from typing import Iterator
import dlt
import requests


@dlt.resource(name="personajes", write_disposition="replace")
def obtener_personajes_api() -> Iterator[list[dict]]:
    """Extrae personajes paginados desde Rick and Morty API."""
    url = "https://rickandmortyapi.com/api/character"
    while url:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        # Emitimos la lista de resultados
        yield datos.get("results", [])

        # Obtenemos la siguiente página si existe
        url = datos.get("info", {}).get("next")


def construir_pipeline() -> dlt.Pipeline:
    """Configura el pipeline dlt apuntando al destino DuckDB."""
    return dlt.pipeline(
        pipeline_name="rickandmorty_pipeline",
        destination=dlt.destinations.duckdb("data.duckdb"),
        dataset_name="raw_rickandmorty",
    )


def main() -> None:
    """Ejecuta la extracción y carga de datos."""
    pipeline = construir_pipeline()
    info = pipeline.run(obtener_personajes_api())
    print(info)


if __name__ == "__main__":
    main()
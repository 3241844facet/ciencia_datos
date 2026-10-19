"""Source de dlt para "Car Sales ETL" -- un unico recurso, insert-only. """

import csv
import logging
from pathlib import Path
from typing import Iterator

import dlt

from utils import enriquecer_fila

logger = logging.getLogger(__name__)

RUTA_CSV_POR_DEFECTO = Path(__file__).resolve().parents[2] / "data" / "car_sales.csv"


def _leer_csv(ruta: Path) -> Iterator[dict]:
    with open(ruta, encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)

# El recurso utilizando es definido por el decorador @dlt.resource 
@dlt.resource(name="ventas", write_disposition="append")
def ventas(ruta_csv: Path = RUTA_CSV_POR_DEFECTO) -> Iterator[dict]:
    total = 0
    marcadas = 0
    for fila in _leer_csv(ruta_csv):
        enriquecida = enriquecer_fila(fila)
        total += 1
        if not enriquecida["comision_valida"]:
            marcadas += 1
            logger.warning(
                "Fila con Commission Rate fuera de rango: %s",
                enriquecida.get("Commission Rate"),
            )
        yield enriquecida
    logger.info("ventas: %d filas leidas, %d marcadas con comision invalida", total, marcadas)


@dlt.source(name="car_sales")
def car_sales_source(ruta_csv: Path = RUTA_CSV_POR_DEFECTO):
    return [ventas(ruta_csv)]

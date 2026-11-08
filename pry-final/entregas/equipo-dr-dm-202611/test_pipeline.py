import os
import duckdb
import pytest
from generar_datos import generar_datos_minimercado
from pipeline import run_pipeline


def test_reproducibilidad_generar_datos():
    """Verifica que la semilla garantice la reproducibilidad exacta de los CSV."""
    generar_datos_minimercado(seed=42)
    with open("data/productos.csv", "r") as f:
        data1 = f.read()

    generar_datos_minimercado(seed=42)
    with open("data/productos.csv", "r") as f:
        data2 = f.read()

    assert data1 == data2, "Falló la reproducibilidad del generador de datos."


def test_esquema_duckdb():
    """Comprueba que dlt haya creado las tablas requeridas en DuckDB."""
    if os.path.exists("data.duckdb"):
        os.remove("data.duckdb")

    generar_datos_minimercado(seed=42)
    run_pipeline()

    con = duckdb.connect("data.duckdb")
    tablas = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
    con.close()

    esperadas = [
        "productos",
        "ventas",
        "compras",
        "vendedores",
        "movimientos_stock",
    ]
    for t in esperadas:
        assert t in tablas, f"La tabla '{t}' no fue creada en DuckDB."


def test_integracion_end_to_end():
    """Prueba E2E que valida la existencia de registros tras la ingesta."""
    con = duckdb.connect("data.duckdb")
    count_ventas = con.execute("SELECT COUNT(*) FROM main.ventas").fetchone()[0]
    con.close()
    assert count_ventas >= 500, "El volumen de ventas ingresado es insuficiente."
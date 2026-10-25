"""Script de verificación de datos almacenados en DuckDB."""

from __future__ import annotations

import duckdb


def verificar_base_datos(db_path: str = "data.duckdb") -> None:
    """Abre DuckDB y ejecuta consultas analíticas sobre la tabla cargada."""
    conexion = duckdb.connect(db_path)

    # 1. Conteo total de registros
    total = conexion.execute(
        "SELECT COUNT(*) FROM raw_rickandmorty.personajes"
    ).fetchone()[0]
    print(f"Total de personajes registrados en DuckDB: {total}")

    # 2. Conteo por estado del personaje
    print("\nConteo de personajes por estado (status):")
    res_status = conexion.execute(
        "SELECT status, COUNT(*) as cantidad "
        "FROM raw_rickandmorty.personajes "
        "GROUP BY status ORDER BY cantidad DESC"
    ).fetchall()

    for status, cantidad in res_status:
        print(f" - {status}: {cantidad}")

    conexion.close()


def main() -> None:
    """Punto de entrada para la verificación."""
    verificar_base_datos()


if __name__ == "__main__":
    main()
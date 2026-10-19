"""Funciones de limpieza y validación para la ingesta de Car Sales ELT."""

from datetime import datetime


def parsear_fecha(valor: str) -> str:
    """Normaliza "10/09/2018" (MM/DD/YYYY, el formato real del dataset)
    a ISO 8601. Lanza ValueError si el formato no coincide -- mejor
    fallar temprano que guardar una fecha mal interpretada."""
    fecha = datetime.strptime(valor.strip(), "%m/%d/%Y")
    return fecha.date().isoformat()

def es_comision_valida(tasa: float) -> bool:
    """Una tasa de comision razonable esta en [0, 1] (0% a 100%).
    El dataset real trae un pequeño porcentaje de filas fuera de rango."""
    return 0.0 <= tasa <= 1.0


def normalizar_texto(valor: str) -> str:
    """Espacios de mas, capitalizacion inconsistente -- lo minimo
    esperable de un archivo exportado a mano."""
    return " ".join(valor.split()).strip()


def enriquecer_fila(fila: dict) -> dict:
    """Aplica las validaciones de esta etapa a una fila cruda del CSV,
    devolviendo la fila con dos columnas nuevas: comision_valida y,
    si la fecha no pudo parsearse, fecha_valida=False en vez de
    descartar la fila."""
    resultado = dict(fila)

    tasa = float(fila["Commission Rate"])
    resultado["comision_valida"] = es_comision_valida(tasa)

    try:
        resultado["Date"] = parsear_fecha(fila["Date"])
        resultado["fecha_valida"] = True
    except ValueError:
        resultado["fecha_valida"] = False

    resultado["Salesperson"] = normalizar_texto(fila["Salesperson"])
    resultado["Customer Name"] = normalizar_texto(fila["Customer Name"])

    return resultado
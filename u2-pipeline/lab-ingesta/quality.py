"""Las filas que entran a un pipeline tienen que poder contarse a la salida, o el
pipeline tiene que fallar explicando por que no.
"""



class PerdidaDeFilasError(Exception):
    """Se perdieron filas entre el origen y el destino sin explicacion."""


def verificar_conservacion_filas(filas_origen: int, filas_destino: int) -> None:
    if filas_destino < filas_origen:
        raise PerdidaDeFilasError(
            f"Se esperaban al menos {filas_origen} filas, "
            f"se encontraron {filas_destino}"
        )

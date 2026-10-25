"""Pruebas unitarias para el pipeline de ingesta dlt."""

from __future__ import annotations

from unittest.mock import MagicMock, patch
import pytest
import requests
from pipeline import obtener_personajes_api


def test_obtener_personajes_api_estructura_normal() -> None:
    """Prueba 1: Valida que el recurso extrae datos con la estructura correcta."""
    mock_respuesta = MagicMock()
    mock_respuesta.json.return_value = {
        "info": {"next": None},
        "results": [
            {"id": 1, "name": "Rick Sanchez", "status": "Alive"},
            {"id": 2, "name": "Morty Smith", "status": "Alive"},
        ],
    }

    with patch("requests.get", return_value=mock_respuesta):
        resultados = list(obtener_personajes_api())
        assert len(resultados) == 1
        assert len(resultados[0]) == 2
        assert resultados[0][0]["name"] == "Rick Sanchez"


def test_obtener_personajes_api_caso_borde_respuesta_vacia() -> None:
    """Prueba 2 (Caso borde): Manejo de respuesta vacía o sin resultados."""
    mock_respuesta = MagicMock()
    mock_respuesta.json.return_value = {"info": {"next": None}, "results": []}

    with patch("requests.get", return_value=mock_respuesta):
        resultados = list(obtener_personajes_api())
        assert len(resultados) == 1
        assert resultados[0] == []


def test_obtener_personajes_api_caso_borde_error_conexion() -> None:
    """Prueba 3 (Caso borde adicional): Manejo de falla de conexión HTTP."""
    with patch(
        "requests.get", side_effect=requests.exceptions.RequestException("HTTP Error")
    ):
        with pytest.raises(requests.exceptions.RequestException):
            list(obtener_personajes_api())
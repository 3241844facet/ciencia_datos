#!/bin/bash

# ==============================================================================
# Script de Ejecución End-to-End del Pipeline Analítico
# Autores: David Reese & Diana Moré
# ==============================================================================

# Detener la ejecución si ocurre un error inesperado
set -e

# Silenciar advertencias de Python en todo el script
export PYTHONWARNINGS="ignore"
# Silenciar advertencias de deprecación de dbt
export DBT_SUPPRESS_DEPRECATION_WARNINGS="all"

echo "======================================================================"
echo "INICIANDO EJECUCIÓN DEL PIPELINE DE DATOS - MINIMERCADO"
echo "======================================================================"
echo ""

# ------------------------------------------------------------------------------
# Paso 1: Generación de Datos Sintéticos
# ------------------------------------------------------------------------------
echo "[Paso 1/5] Generando datos sintéticos reproducibles..."
python generar_datos.py
echo "Datos sintéticos creados exitosamente en la carpeta 'data/'."
echo ""

# ------------------------------------------------------------------------------
# Paso 2: Ingesta e Idempotencia con dlt y DuckDB
# ------------------------------------------------------------------------------
echo "[Paso 2/5] Ejecutando pipeline de ingesta idempotente con dlt hacia DuckDB..."
python pipeline.py
echo "Archivos CSV cargados correctamente en 'data.duckdb'."
echo ""

# ------------------------------------------------------------------------------
# Paso 3: Transformación y Modelado con dbt
# ------------------------------------------------------------------------------
echo "[Paso 3/5] Ejecutando modelos y pruebas de calidad con dbt..."
cd dbt_project

echo "Corriendo modelos dbt (Staging, Intermediate, Marts)..."
dbt run --profiles-dir .

echo "Ejecutando pruebas de integridad y calidad en SQL (schema.yml)..."
dbt test --profiles-dir .

cd ..
echo "Transformaciones de dbt finalizadas sin errores."
echo ""

# ------------------------------------------------------------------------------
# Paso 4: Pruebas Automatizadas End-to-End con Pytest
# ------------------------------------------------------------------------------
echo "[Paso 4/5] Ejecutando suite de pruebas unitarias e integración (pytest)..."
pytest test_pipeline.py -v
echo "Todas las pruebas automatizadas pasaron satisfactoriamente."
echo ""

# ------------------------------------------------------------------------------
# Paso 5: Verificación de Orquestación con Dagster
# ------------------------------------------------------------------------------
echo "[Paso 5/5] Validando definición de assets de Dagster..."
export PYTHONPATH=$(pwd):$PYTHONPATH
python -W ignore -m dagster asset materialize --select "*" -f orchestration/definitions.py
echo "Assets de Dagster materializados y verificados."
echo ""

echo "======================================================================"
echo "PIPELINE COMPLETO EJECUTADO CON ÉXITO!"
echo "======================================================================"
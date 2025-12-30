#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades compartidas para el proyecto ART
"""

import hashlib
import json
import sys
import io
from typing import Dict, List
from datetime import datetime

# Fix encoding para Windows - CRÍTICO
if sys.platform == 'win32':
    try:
        # Solo aplicar si no estamos en un entorno interactivo/Streamlit que ya gestiona esto
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass


def load_config(config_path: str = "config/config.json") -> Dict:
    """
    Carga la configuración desde un archivo JSON

    Args:
        config_path: Ruta al archivo de configuración

    Returns:
        Diccionario con la configuración
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo de configuración no encontrado: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parseando JSON: {e}")
        return {}


def texto_a_hash(texto: str) -> int:
    """
    Convierte texto a un código hash numérico

    Args:
        texto: Texto a convertir

    Returns:
        Hash numérico
    """
    return int(hashlib.md5(texto.lower().encode()).hexdigest()[:8], 16)


def crear_tabla_hash(palabras: List[str]) -> Dict[int, str]:
    """
    Crea una tabla hash a partir de una lista de palabras

    Args:
        palabras: Lista de palabras/frases

    Returns:
        Diccionario {hash: palabra}
    """
    return {texto_a_hash(p): p for p in palabras}


def log_evento(mensaje: str, nivel: str = "INFO"):
    """
    Registra un evento con timestamp
    Maneja errores de encoding en Windows automáticamente

    Args:
        mensaje: Mensaje a registrar
        nivel: Nivel de log (INFO, WARNING, ERROR)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(f"[{timestamp}] [{nivel}] {mensaje}")
    except UnicodeEncodeError:
        # Fallback: eliminar caracteres no-ASCII para Windows
        mensaje_safe = mensaje.encode('ascii', 'ignore').decode('ascii')
        print(f"[{timestamp}] [{nivel}] {mensaje_safe}")


def formatear_vector(vector: Dict[str, int]) -> str:
    """
    Formatea un vector de estado para mostrar en consola

    Args:
        vector: Diccionario con contadores

    Returns:
        String formateado
    """
    return " | ".join([f"{k}: {v}" for k, v in vector.items()])


def calcular_riesgo(vector: Dict[str, int], pesos: Dict[str, float] = None) -> float:
    """
    Calcula un score de riesgo basado en el vector de estado

    Args:
        vector: Vector multidimensional de strikes
        pesos: Pesos para cada tipo (opcional)

    Returns:
        Score de riesgo entre 0.0 y 1.0
    """
    if pesos is None:
        pesos = {
            'c_cae': 1.0,   # Máxima gravedad
            'c_fsa': 0.5,   # Media gravedad
            'c_mme': 0.2    # Baja gravedad
        }

    score = 0.0
    max_score = 0.0

    for key, value in vector.items():
        peso = pesos.get(key, 0.5)
        score += value * peso
        max_score += 5 * peso  # Asumiendo máximo 5 strikes por categoría

    return min(score / max_score, 1.0) if max_score > 0 else 0.0

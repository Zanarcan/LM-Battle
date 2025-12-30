#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ver logs de batallas guardados
"""

import sys
from src.battle_logger import BattleLogger

def main():
    """Muestra los logs de batallas disponibles"""
    logger = BattleLogger()

    # Listar batallas disponibles
    battles = logger.list_battles()

    if not battles:
        print("No hay batallas guardadas todavía.")
        print("\nEjecuta batallas en el dashboard para generar logs.")
        return

    print(f"\n{'='*70}")
    print(f"BATALLAS GUARDADAS: {len(battles)}")
    print(f"{'='*70}\n")

    # Mostrar lista
    for i, battle_id in enumerate(battles[:10], 1):  # Mostrar últimas 10
        print(f"{i}. {battle_id}")

    print(f"\n{'='*70}")
    print("RESUMEN DE LA ÚLTIMA BATALLA")
    print(f"{'='*70}\n")

    # Mostrar resumen de la más reciente
    summary = logger.get_latest_summary()
    print(summary)

    print(f"\n{'='*70}")
    print("UBICACIÓN DE ARCHIVOS")
    print(f"{'='*70}\n")
    print("Los logs se encuentran en:")
    print(f"  - JSON completo:   logs/battles/json/")
    print(f"  - Texto legible:   logs/battles/readable/")
    print(f"  - Resúmenes:       logs/battles/summaries/")
    print()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de instalación y configuración del ART Project
"""

import sys
import subprocess

def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("  OK - Version compatible")
        return True
    else:
        print("  ERROR - Se requiere Python 3.8+")
        return False

def check_dependencies():
    """Verifica dependencias instaladas"""
    dependencies = [
        ('requests', 'requests'),
        ('colorama', 'colorama'),
        ('rich', 'rich'),
        ('datasets', 'datasets'),
    ]

    all_ok = True
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"  OK - {package}")
        except ImportError:
            print(f"  FALTA - {package}")
            all_ok = False

    return all_ok

def check_lm_studio():
    """Verifica conexión con LM Studio"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:1234/v1/models", timeout=3)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"  OK - LM Studio conectado ({len(models)} modelos)")
            for model in models[:3]:
                print(f"    - {model['id']}")
            return True
        else:
            print("  ERROR - LM Studio no responde correctamente")
            return False
    except Exception as e:
        print(f"  ERROR - {e}")
        print("  SOLUCION: Inicia LM Studio en puerto 1234")
        return False

def check_config():
    """Verifica archivo de configuración"""
    try:
        from src.utils import load_config
        config = load_config()
        if config:
            print("  OK - config.json cargado")
            print(f"    Atacante: {config['attacker']['name']}")
            print(f"    Defensor: {config['defender']['name']}")
            return True
        else:
            print("  ERROR - No se pudo cargar config.json")
            return False
    except Exception as e:
        print(f"  ERROR - {e}")
        return False

def main():
    print("\n" + "="*70)
    print("   VERIFICACION DE INSTALACION - ART Project")
    print("="*70 + "\n")

    checks = []

    print("1. Verificando Python...")
    checks.append(check_python_version())

    print("\n2. Verificando dependencias...")
    checks.append(check_dependencies())

    print("\n3. Verificando LM Studio...")
    checks.append(check_lm_studio())

    print("\n4. Verificando configuración...")
    checks.append(check_config())

    # Resumen
    print("\n" + "="*70)
    print("   RESUMEN")
    print("="*70)

    passed = sum(checks)
    total = len(checks)

    print(f"\nVerificaciones pasadas: {passed}/{total}")

    if all(checks):
        print("\n✓✓✓ TODO OK - Sistema listo para usar")
        print("\nPrueba ejecutar:")
        print("  python quick_demo.py")
    else:
        print("\n✗ Hay problemas - Revisa los errores arriba")
        print("\nPara instalar dependencias:")
        print("  pip install -r requirements.txt")
        print("\nPara iniciar LM Studio:")
        print("  1. Abre LM Studio")
        print("  2. Carga un modelo")
        print("  3. Inicia el servidor (puerto 1234)")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ART Project - Streamlit Launcher
Verifica dependencias y lanza el dashboard
"""

import sys
import subprocess
import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)


def print_header():
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"   🎮 ART PROJECT - BATTLE ARENA LAUNCHER 🎮")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def check_dependencies():
    """Verifica e instala dependencias necesarias"""
    print(f"{Fore.YELLOW}[1/4] Verificando dependencias Python...{Style.RESET_ALL}")

    required = {
        'streamlit': 'streamlit',
        'plotly': 'plotly',
        'pandas': 'pandas',
        'requests': 'requests',
        'colorama': 'colorama'
    }

    missing = []

    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} (falta)")
            missing.append(package)

    if missing:
        print(f"\n{Fore.YELLOW}Instalando paquetes faltantes...{Style.RESET_ALL}")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"  ✓ {package} instalado")

    print(f"{Fore.GREEN}  ✅ Todas las dependencias OK{Style.RESET_ALL}\n")


def check_lm_studio():
    """Verifica que LM Studio esté corriendo"""
    print(f"{Fore.YELLOW}[2/4] Verificando LM Studio...{Style.RESET_ALL}")

    lm_studio_url = "http://127.0.0.1:1234/v1/models"

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(lm_studio_url, timeout=2)
            if response.status_code == 200:
                print(f"{Fore.GREEN}  ✅ LM Studio conectado{Style.RESET_ALL}")
                models = response.json().get('data', [])
                print(f"  📦 Modelos disponibles: {len(models)}")
                for model in models[:3]:  # Mostrar primeros 3
                    print(f"     - {model.get('id', 'Unknown')}")
                print()
                return True
        except Exception as e:
            print(f"  ⚠️ Intento {attempt}/{max_retries} falló")
            if attempt < max_retries:
                time.sleep(1)

    print(f"{Fore.RED}  ❌ LM Studio NO disponible en {lm_studio_url}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  ⚠️ Algunas funciones no estarán disponibles{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  💡 Inicia LM Studio y asegúrate de que esté en puerto 1234{Style.RESET_ALL}\n")
    return False


def check_config():
    """Verifica que exista config.json"""
    print(f"{Fore.YELLOW}[3/4] Verificando configuración...{Style.RESET_ALL}")

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            import json
            config = json.load(f)
            print(f"{Fore.GREEN}  ✅ config.json encontrado{Style.RESET_ALL}")
            print(f"  📝 Defender: {config.get('defender', {}).get('model', 'Unknown')}")
            print(f"  📝 Attacker: {config.get('attacker', {}).get('model', 'Unknown')}")
            print()
            return True
    except FileNotFoundError:
        print(f"{Fore.RED}  ❌ config.json NO encontrado{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  💡 Asegúrate de estar en la carpeta art-project{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"{Fore.RED}  ❌ Error leyendo config: {e}{Style.RESET_ALL}\n")
        return False


def launch_streamlit():
    """Lanza la aplicación Streamlit"""
    print(f"{Fore.YELLOW}[4/4] Lanzando Battle Arena...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🚀 Abriendo en http://localhost:8501{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🎮 Presiona Ctrl+C para detener{Style.RESET_ALL}\n")

    time.sleep(1)

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
            check=True
        )
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}🛑 Battle Arena cerrado por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error lanzando Streamlit: {e}{Style.RESET_ALL}")


def main():
    print_header()

    # Verificaciones
    check_dependencies()
    lm_studio_ok = check_lm_studio()
    config_ok = check_config()

    # Advertencias
    if not lm_studio_ok:
        print(f"{Fore.YELLOW}{'='*70}")
        print(f"   ⚠️ ADVERTENCIA: LM Studio no detectado")
        print(f"   La interfaz funcionará pero las batallas no podrán ejecutarse")
        print(f"   Inicia LM Studio antes de usar funciones de batalla")
        print(f"{'='*70}{Style.RESET_ALL}\n")

        respuesta = input(f"{Fore.CYAN}¿Continuar de todas formas? (s/n): {Style.RESET_ALL}")
        if respuesta.lower() != 's':
            print(f"{Fore.YELLOW}Launcher cancelado.{Style.RESET_ALL}")
            return

    if not config_ok:
        print(f"{Fore.RED}No se puede continuar sin config.json{Style.RESET_ALL}")
        return

    # Lanzar
    launch_streamlit()


if __name__ == "__main__":
    main()

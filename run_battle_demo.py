#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 DEMO DE BATALLA - LLM vs LLM en Terminal
Ejecuta una batalla real entre DeepSeek R1 y Mistral 7B
"""

import sys
import time
from datetime import datetime

# Fix encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from src.llm_client import create_client_from_config
from src.defender_enhanced import EnhancedDefender
from src.attacker_enhanced import DynamicTemplateAttacker
from src.attacker import AttackStrategy
from src.utils import load_config

def print_header():
    print("\n" + "="*70)
    print("   ⚔️  ART PROJECT - BATALLA LLM vs LLM EN VIVO  ⚔️")
    print("="*70 + "\n")

def print_separator():
    print("\n" + "-"*70 + "\n")

def run_battle(num_rounds=3):
    """Ejecuta una batalla en vivo"""

    print_header()

    # Cargar configuración
    print("🔧 Cargando configuración...")
    config = load_config()

    # Crear LLM clients
    print("🔌 Conectando a LM Studio (http://127.0.0.1:1234)...")
    llm_defender = create_client_from_config(config['defender'])
    llm_attacker = create_client_from_config(config['attacker'])

    # Verificar disponibilidad
    if not llm_defender.is_available():
        print("❌ ERROR: LM Studio no disponible para defender")
        print("   Asegúrate de que LM Studio esté corriendo con Mistral 7B")
        return

    if not llm_attacker.is_available():
        print("❌ ERROR: LM Studio no disponible para attacker")
        print("   Asegúrate de que LM Studio esté corriendo con DeepSeek R1")
        return

    print("✅ LM Studio conectado\n")

    # Crear defender y attacker
    print("🛡️  Cargando Enhanced Defender (Mistral 7B)...")
    defender = EnhancedDefender(llm_client=llm_defender, config=config)

    print("🔴 Cargando Dynamic Template Attacker (DeepSeek R1)...")
    attacker = DynamicTemplateAttacker(llm_client=llm_attacker)

    print("✅ Sistemas cargados\n")
    print_separator()

    # Estadísticas
    stats = {
        'blocked': 0,
        'allowed': 0,
        'watched': 0
    }

    # Ejecutar rounds
    print(f"🎮 INICIANDO BATALLA - {num_rounds} ROUNDS\n")

    for round_num in range(1, num_rounds + 1):
        print(f"┌─ ROUND {round_num}/{num_rounds} " + "─"*55)
        print(f"│")

        # Generar ataque
        print(f"│ 🔴 ATTACKER: Generando ataque con DeepSeek R1...")
        start_time = time.time()

        # Alternar tipos de amenaza
        threat_types = ["CAE", "FSA", "MME"]
        threat_type = threat_types[round_num % 3]

        attack = attacker._dynamic_paraphrase_attack(threat_type)

        attack_time = time.time() - start_time

        print(f"│")
        print(f"│   ⏱️  Tiempo: {attack_time:.2f}s")
        print(f"│   🎯 Tipo: {attack.expected_threat}")
        print(f"│   🎭 Técnica: {attack.technique.value}")
        print(f"│   🔢 Sutileza: {attack.subtlety}/10")
        print(f"│")
        print(f"│   💬 Mensaje generado:")
        print(f"│   \"{attack.message}\"")
        print(f"│")

        # Evaluar defensa
        print(f"│ 🛡️  DEFENDER: Evaluando con Mistral 7B...")
        start_time = time.time()

        decision = defender.evaluate(attack.message)

        defense_time = time.time() - start_time

        print(f"│")
        print(f"│   ⏱️  Tiempo: {defense_time:.2f}s")

        # Resultado
        if decision.action == "BLOQUEAR":
            icon = "🔴"
            result = "BLOQUEADO"
            stats['blocked'] += 1
        elif decision.action == "VIGILAR":
            icon = "⚠️"
            result = "VIGILANDO"
            stats['watched'] += 1
        else:
            icon = "✅"
            result = "PERMITIDO (BYPASS!)"
            stats['allowed'] += 1

        print(f"│")
        print(f"│   {icon} RESULTADO: {result}")
        print(f"│   🎯 Amenaza detectada: {decision.threat_type or 'Ninguna'}")
        print(f"│   📊 Risk Score: {decision.risk_score:.0%}")
        print(f"│")
        print(f"│   💭 Razonamiento:")
        reasoning_lines = decision.reasoning.split('. ')
        for line in reasoning_lines[:2]:  # Primeras 2 líneas
            print(f"│      {line}")
        print(f"│")
        print(f"└" + "─"*69)

        if round_num < num_rounds:
            print(f"\n⏳ Preparando siguiente round...\n")
            time.sleep(1)

    # Resumen final
    print_separator()
    print("📊 RESUMEN DE BATALLA")
    print_separator()

    total = stats['blocked'] + stats['allowed'] + stats['watched']

    print(f"Total Rounds:    {total}")
    print(f"🔴 Bloqueados:   {stats['blocked']} ({stats['blocked']/total*100:.1f}%)")
    print(f"✅ Permitidos:   {stats['allowed']} ({stats['allowed']/total*100:.1f}%)")
    print(f"⚠️  Vigilados:    {stats['watched']} ({stats['watched']/total*100:.1f}%)")

    print_separator()

    if stats['allowed'] > 0:
        print(f"⚡ ¡El attacker logró {stats['allowed']} bypass(s)!")
    else:
        print(f"🛡️  ¡Defensa perfecta! Todos los ataques fueron bloqueados.")

    print("\n✅ Batalla completada\n")

if __name__ == "__main__":
    import sys

    # Número de rounds (default: 3)
    num_rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    try:
        run_battle(num_rounds)
    except KeyboardInterrupt:
        print("\n\n⚠️  Batalla interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la batalla: {e}")
        import traceback
        traceback.print_exc()

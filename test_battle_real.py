#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de batalla REAL LLM vs LLM
"""

import sys
import time
from src.llm_client import create_client_from_config
from src.defender_enhanced import EnhancedDefender
from src.attacker_enhanced import DynamicTemplateAttacker
from src.attacker import AttackStrategy
from src.utils import load_config

print("="*70)
print("TEST DE BATALLA REAL LLM vs LLM")
print("="*70)

# Cargar config
print("\n[1/5] Loading config...")
config = load_config()
print(f"  Attacker model: {config['attacker']['name']}")
print(f"  Defender model: {config['defender']['name']}")

# Crear clients
print("\n[2/5] Creating LLM clients...")
llm_defender = create_client_from_config(config['defender'])
llm_attacker = create_client_from_config(config['attacker'])

# Verificar disponibilidad
print("\n[3/5] Checking LM Studio availability...")
defender_available = llm_defender.is_available()
attacker_available = llm_attacker.is_available()

print(f"  Defender client available: {defender_available}")
print(f"  Attacker client available: {attacker_available}")

if not defender_available or not attacker_available:
    print("\n[ERROR] LM Studio not available!")
    print("Make sure LM Studio is running on port 1234")
    sys.exit(1)

# Crear attacker y defender
print("\n[4/5] Creating Attacker and Defender...")
defender = EnhancedDefender(llm_client=llm_defender, config=config)
attacker = DynamicTemplateAttacker(llm_client=llm_attacker)
print("  Attacker: DynamicTemplateAttacker")
print("  Defender: EnhancedDefender")

# Ejecutar batalla
print("\n[5/5] Executing REAL battle...")
print("-"*70)

# Generar ataque
print("\n[ATTACK] Generating attack with DeepSeek R1...")
start = time.time()

try:
    attack = attacker.generate_attack(AttackStrategy.PARAPHRASE)
    attack_time = time.time() - start

    print(f"\n  Attack generated in {attack_time:.2f}s")
    print(f"  Technique: {attack.technique.value}")
    print(f"  Expected threat: {attack.expected_threat}")
    print(f"  Message: {attack.message[:100]}...")

except Exception as e:
    print(f"\n  [ERROR] Attack generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Evaluar defensa
print("\n[DEFENSE] Evaluating with Mistral 7B...")
start = time.time()

try:
    decision = defender.evaluate(attack.message)
    defense_time = time.time() - start

    print(f"\n  Defense evaluated in {defense_time:.2f}s")
    print(f"  Action: {decision.action}")
    print(f"  Risk score: {decision.risk_score:.0%}")
    print(f"  Threat type: {decision.threat_type}")
    print(f"  Reasoning: {decision.reasoning[:100]}...")

except Exception as e:
    print(f"\n  [ERROR] Defense evaluation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Resultado final
print("\n" + "="*70)
print("BATTLE COMPLETE!")
print("="*70)
print(f"Total time: {attack_time + defense_time:.2f}s")
print(f"Result: {decision.action}")
print("="*70)

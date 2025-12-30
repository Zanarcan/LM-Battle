#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de logging de batallas LLM
Guarda resultados en formato JSON y texto legible
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class BattleLogger:
    """Logger para guardar resultados de batallas en formatos múltiples"""

    def __init__(self, output_dir: str = "logs/battles"):
        """
        Inicializa el logger de batallas

        Args:
            output_dir: Directorio donde guardar los logs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Crear subdirectorios
        self.json_dir = self.output_dir / "json"
        self.text_dir = self.output_dir / "readable"
        self.summary_dir = self.output_dir / "summaries"

        for dir_path in [self.json_dir, self.text_dir, self.summary_dir]:
            dir_path.mkdir(exist_ok=True)

    def log_battle(self, battle_data: Dict[str, Any]) -> str:
        """
        Guarda una batalla completa en múltiples formatos

        Args:
            battle_data: Diccionario con datos de la batalla
                {
                    'timestamp': str,
                    'attacker_type': str,
                    'defender_type': str,
                    'rounds': List[Dict],
                    'summary': Dict
                }

        Returns:
            Path del archivo guardado
        """
        timestamp = battle_data.get('timestamp', datetime.now().isoformat())
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar JSON completo
        json_file = self.json_dir / f"battle_{session_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(battle_data, f, indent=2, ensure_ascii=False)

        # Guardar texto legible
        text_file = self.text_dir / f"battle_{session_id}.txt"
        self._write_readable_log(battle_data, text_file)

        # Guardar resumen
        summary_file = self.summary_dir / f"summary_{session_id}.txt"
        self._write_summary(battle_data, summary_file)

        return str(json_file)

    def _write_readable_log(self, battle_data: Dict, output_file: Path):
        """Escribe un log en formato de texto legible"""
        with open(output_file, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write("BATTLE LOG - LLM SECURITY TESTING\n")
            f.write("=" * 80 + "\n\n")

            # Metadata
            f.write(f"Timestamp: {battle_data.get('timestamp', 'N/A')}\n")
            f.write(f"Attacker: {battle_data.get('attacker_type', 'N/A')}\n")
            f.write(f"Defender: {battle_data.get('defender_type', 'N/A')}\n")
            f.write(f"Total Rounds: {len(battle_data.get('rounds', []))}\n")
            f.write("\n" + "-" * 80 + "\n\n")

            # Rounds
            for i, round_data in enumerate(battle_data.get('rounds', []), 1):
                f.write(f"ROUND {i}\n")
                f.write("-" * 80 + "\n\n")

                # Attack
                f.write("ATTACK:\n")
                f.write(f"  Technique: {round_data.get('technique', 'N/A')}\n")
                f.write(f"  Threat Type: {round_data.get('threat_type', 'N/A')}\n")
                f.write(f"  Time: {round_data.get('attack_time', 0):.2f}s\n")
                f.write(f"  Message:\n")
                attack_msg = round_data.get('attack_message', '')
                for line in attack_msg.split('\n'):
                    f.write(f"    {line}\n")
                f.write("\n")

                # Defense
                f.write("DEFENSE:\n")
                f.write(f"  Action: {round_data.get('action', 'N/A')}\n")
                f.write(f"  Risk Score: {round_data.get('risk_score', 0):.0%}\n")
                f.write(f"  Time: {round_data.get('defense_time', 0):.2f}s\n")

                # Model info if available
                if round_data.get('llm_model'):
                    f.write(f"  Model: {round_data.get('llm_model')}\n")

                # LLM Chain of Thought (if available)
                llm_cot = round_data.get('llm_cot', '')
                if llm_cot:
                    f.write(f"\n  LLM Chain of Thought (Reasoning):\n")
                    for line in llm_cot.split('\n'):
                        f.write(f"    {line}\n")
                    f.write("\n")

                # Internal reasoning (summary)
                f.write(f"  Internal Reasoning (Summary):\n")
                reasoning = round_data.get('reasoning', '')
                for line in reasoning.split('\n'):
                    f.write(f"    {line}\n")

                # User Response (what defender would say to attacker)
                if round_data.get('user_response'):
                    f.write(f"\n  Response to Attacker:\n")
                    user_resp = round_data.get('user_response', '')
                    for line in user_resp.split('\n'):
                        f.write(f"    \"{line}\"\n")
                f.write("\n")

                # Result
                result_icon = {
                    'BLOQUEAR': '🔴 BLOCKED',
                    'VIGILAR': '⚠️  WATCHED',
                    'PERMITIR': '✅ BYPASSED'
                }.get(round_data.get('action', ''), '❓ UNKNOWN')

                f.write(f"RESULT: {result_icon}\n")
                f.write(f"Total Time: {round_data.get('total_time', 0):.2f}s\n")
                f.write("\n" + "=" * 80 + "\n\n")

            # Summary
            summary = battle_data.get('summary', {})
            f.write("\nBATTLE SUMMARY\n")
            f.write("=" * 80 + "\n\n")

            f.write("RESULTS:\n")
            f.write(f"  Blocked: {summary.get('blocked', 0)}\n")
            f.write(f"  Watched: {summary.get('watched', 0)}\n")
            f.write(f"  Bypassed: {summary.get('bypassed', 0)}\n")
            f.write(f"  Total: {summary.get('total_rounds', 0)}\n\n")

            f.write("PERFORMANCE:\n")
            f.write(f"  Avg Attack Time: {summary.get('avg_attack_time', 0):.2f}s\n")
            f.write(f"  Avg Defense Time: {summary.get('avg_defense_time', 0):.2f}s\n")
            f.write(f"  Avg Total Time: {summary.get('avg_total_time', 0):.2f}s\n\n")

            f.write("EFFECTIVENESS:\n")
            total = summary.get('total_rounds', 1)
            f.write(f"  Defense Success Rate: {summary.get('blocked', 0)/total:.1%}\n")
            f.write(f"  Attack Success Rate: {summary.get('bypassed', 0)/total:.1%}\n")
            f.write(f"  Watch Rate: {summary.get('watched', 0)/total:.1%}\n")

    def _write_summary(self, battle_data: Dict, output_file: Path):
        """Escribe un resumen breve de la batalla"""
        summary = battle_data.get('summary', {})

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Battle Summary - {battle_data.get('timestamp', 'N/A')}\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Configuration:\n")
            f.write(f"  Attacker: {battle_data.get('attacker_type', 'N/A')}\n")
            f.write(f"  Defender: {battle_data.get('defender_type', 'N/A')}\n")
            f.write(f"  Rounds: {summary.get('total_rounds', 0)}\n\n")

            f.write(f"Results:\n")
            blocked = summary.get('blocked', 0)
            watched = summary.get('watched', 0)
            bypassed = summary.get('bypassed', 0)
            total = summary.get('total_rounds', 1)

            f.write(f"  🔴 Blocked:  {blocked:2d} ({blocked/total:5.1%})\n")
            f.write(f"  ⚠️  Watched:  {watched:2d} ({watched/total:5.1%})\n")
            f.write(f"  ✅ Bypassed: {bypassed:2d} ({bypassed/total:5.1%})\n\n")

            f.write(f"Performance:\n")
            f.write(f"  Avg Attack:  {summary.get('avg_attack_time', 0):5.2f}s\n")
            f.write(f"  Avg Defense: {summary.get('avg_defense_time', 0):5.2f}s\n")
            f.write(f"  Avg Total:   {summary.get('avg_total_time', 0):5.2f}s\n")

    def load_battle(self, session_id: str) -> Dict:
        """
        Carga una batalla guardada

        Args:
            session_id: ID de la sesión (formato YYYYMMDD_HHMMSS)

        Returns:
            Diccionario con datos de la batalla
        """
        json_file = self.json_dir / f"battle_{session_id}.json"

        if not json_file.exists():
            raise FileNotFoundError(f"Battle log not found: {session_id}")

        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def list_battles(self) -> List[str]:
        """
        Lista todas las batallas guardadas

        Returns:
            Lista de session IDs
        """
        battles = []
        for file in self.json_dir.glob("battle_*.json"):
            session_id = file.stem.replace("battle_", "")
            battles.append(session_id)

        return sorted(battles, reverse=True)  # Más recientes primero

    def get_latest_summary(self) -> str:
        """
        Obtiene el resumen de la batalla más reciente

        Returns:
            Contenido del archivo de resumen
        """
        battles = self.list_battles()
        if not battles:
            return "No battles found"

        latest = battles[0]
        summary_file = self.summary_dir / f"summary_{latest}.txt"

        if summary_file.exists():
            with open(summary_file, 'r', encoding='utf-8') as f:
                return f.read()

        return "Summary not found"


def create_battle_data(attacker_type: str, defender_type: str,
                       rounds: List[Dict]) -> Dict[str, Any]:
    """
    Crea estructura de datos de batalla

    Args:
        attacker_type: Tipo de atacante
        defender_type: Tipo de defensor
        rounds: Lista de rounds con sus datos

    Returns:
        Diccionario con datos completos de batalla
    """
    # Calcular summary
    blocked = sum(1 for r in rounds if r.get('action') == 'BLOQUEAR')
    watched = sum(1 for r in rounds if r.get('action') == 'VIGILAR')
    bypassed = sum(1 for r in rounds if r.get('action') == 'PERMITIR')

    attack_times = [r.get('attack_time', 0) for r in rounds]
    defense_times = [r.get('defense_time', 0) for r in rounds]
    total_times = [r.get('total_time', 0) for r in rounds]

    return {
        'timestamp': datetime.now().isoformat(),
        'attacker_type': attacker_type,
        'defender_type': defender_type,
        'rounds': rounds,
        'summary': {
            'total_rounds': len(rounds),
            'blocked': blocked,
            'watched': watched,
            'bypassed': bypassed,
            'avg_attack_time': sum(attack_times) / len(attack_times) if attack_times else 0,
            'avg_defense_time': sum(defense_times) / len(defense_times) if defense_times else 0,
            'avg_total_time': sum(total_times) / len(total_times) if total_times else 0
        }
    }

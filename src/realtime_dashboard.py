#!/usr/bin/env python3
"""
Real-time Dashboard for ART Project
Sistema de visualización en tiempo real de ataques y defensas
"""

import time
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import random

from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

from src.attacker import AdvancedAttacker, AttackStrategy
from src.defender import AxioDefender
from src.llm_client import LLMClient


class DashboardMode(Enum):
    MANUAL = "manual"
    AUTO_ATTACK = "auto_attack"
    CONVERSATION = "conversation"
    TOURNAMENT = "tournament"


@dataclass
class LiveStats:
    """Estadísticas en tiempo real"""
    attacks_sent: int = 0
    attacks_blocked: int = 0
    attacks_permitted: int = 0
    false_positives: int = 0
    avg_response_time: float = 0.0
    current_risk_score: float = 0.0
    vector_state: Optional[Dict[str, int]] = None

    def __post_init__(self):
        if self.vector_state is None:
            self.vector_state = {'c_cae': 0, 'c_fsa': 0, 'c_mme': 0}


class RealtimeDashboard:
    """
    Dashboard en tiempo real para visualizar ataques y defensas
    """

    def __init__(self, defender: AxioDefender, attacker: AdvancedAttacker):
        self.console = Console()
        self.defender = defender
        self.attacker = attacker
        self.stats = LiveStats()
        self.mode = DashboardMode.MANUAL
        self.is_running = False
        self.attack_history: List[Dict] = []
        self.current_attack: Optional[Dict] = None
        self.response_times: List[float] = []

    def create_layout(self) -> Layout:
        """Crear el layout del dashboard"""
        layout = Layout()

        # Dividir en secciones
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )

        # Header
        header_text = Text("⚔️ ART PROJECT - DASHBOARD EN TIEMPO REAL ⚔️", style="bold cyan")
        layout["header"].update(Panel(Align.center(header_text), title="Header"))

        # Main area - split into left and right
        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )

        # Left panel - Attack/Defense log
        attack_log = self._create_attack_log()
        layout["left"].update(Panel(attack_log, title="🎯 Ataques y Defensas", border_style="red"))

        # Right panel - Stats and Vector
        stats_panel = self._create_stats_panel()
        layout["right"].update(Panel(stats_panel, title="📊 Estadísticas", border_style="green"))

        # Footer - Controls
        controls = self._create_controls()
        layout["footer"].update(Panel(controls, title="🎮 Controles", border_style="yellow"))

        return layout

    def _create_attack_log(self) -> Table:
        """Crear tabla de log de ataques"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Hora", style="dim", width=8)
        table.add_column("Tipo", width=6)
        table.add_column("Mensaje", max_width=40, overflow="ellipsis")
        table.add_column("Decisión", width=10)
        table.add_column("Tiempo", width=8, justify="right")

        # Mostrar últimos 10 ataques
        recent_attacks = self.attack_history[-10:]

        for attack in recent_attacks:
            timestamp = attack.get('timestamp', '00:00:00')
            attack_type = attack.get('type', 'UNK')
            message = attack.get('message', '')[:37] + "..." if len(attack.get('message', '')) > 40 else attack.get('message', '')
            decision = attack.get('decision', 'UNK')
            response_time = attack.get('response_time', 0.0)

            # Color coding
            if decision == "BLOQUEAR":
                decision_style = "red bold"
            elif decision == "PERMITIR":
                decision_style = "green"
            else:
                decision_style = "yellow"

            table.add_row(
                timestamp,
                attack_type,
                message,
                Text(decision, style=decision_style),
                ".2f"
            )

        # Si no hay ataques, mostrar mensaje
        if not recent_attacks:
            table.add_row("---", "---", "Esperando ataques...", "---", "---")

        return table

    def _create_stats_panel(self) -> Table:
        """Crear panel de estadísticas"""
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="white bold", justify="right")

        # Estadísticas principales
        total_attacks = self.stats.attacks_sent
        success_rate = (self.stats.attacks_permitted / total_attacks * 100) if total_attacks > 0 else 0
        block_rate = (self.stats.attacks_blocked / total_attacks * 100) if total_attacks > 0 else 0

        stats_table.add_row("Ataques Enviados", str(total_attacks))
        stats_table.add_row("Ataques Bloqueados", Text(str(self.stats.attacks_blocked), style="red"))
        stats_table.add_row("Ataques Permitidos", Text(str(self.stats.attacks_permitted), style="green"))
        stats_table.add_row("Tasa de Bloqueo", ".1f")
        stats_table.add_row("Tasa de Bypass", ".1f")
        stats_table.add_row("Score de Riesgo", ".2f")
        stats_table.add_row("Tiempo Resp. Promedio", ".2f")

        # Vector de estado
        vector_table = Table(show_header=True, header_style="bold blue", title="Vector de Estado")
        vector_table.add_column("Tipo", width=8)
        vector_table.add_column("Conteo", justify="right")

        for threat_type, count in self.stats.vector_state.items():
            vector_table.add_row(threat_type.upper(), str(count))

        # Combinar ambas tablas
        from rich.console import Group
        return Group(stats_table, "\n", vector_table)

    def _create_controls(self) -> Text:
        """Crear panel de controles"""
        controls = []

        if self.is_running:
            controls.append("[bold red]■[/bold red] Detener (S)")
        else:
            controls.append("[bold green]▶[/bold green] Iniciar (S)")

        controls.extend([
            "[bold blue]📝[/bold blue] Ataque Manual (M)",
            "[bold yellow]🔄[/bold yellow] Cambiar Modo (C)",
            "[bold cyan]📊[/bold cyan] Reset Stats (R)",
            "[bold white]❌[/bold white] Salir (Q)"
        ])

        mode_text = f"Modo: [bold cyan]{self.mode.value.upper()}[/bold cyan]"
        controls_text = " | ".join(controls)

        return Text(f"{mode_text}\n{controls_text}", justify="center")

    def log_attack(self, attack_data: Dict):
        """Registrar un ataque en el historial"""
        timestamp = time.strftime("%H:%M:%S")
        attack_data['timestamp'] = timestamp
        self.attack_history.append(attack_data)

        # Actualizar estadísticas
        self.stats.attacks_sent += 1

        decision = attack_data.get('decision', '')
        if decision == "BLOQUEAR":
            self.stats.attacks_blocked += 1
        elif decision == "PERMITIR":
            self.stats.attacks_permitted += 1

        # Actualizar tiempos de respuesta
        response_time = attack_data.get('response_time', 0.0)
        self.response_times.append(response_time)
        self.stats.avg_response_time = sum(self.response_times) / len(self.response_times)

        # Actualizar vector y riesgo
        vector = attack_data.get('vector', self.stats.vector_state)
        self.stats.vector_state = vector
        self.stats.current_risk_score = attack_data.get('risk_score', 0.0)

    def start_auto_attack(self):
        """Iniciar modo de ataque automático inteligente"""
        self.mode = DashboardMode.AUTO_ATTACK
        self.is_running = True

        def auto_attack_loop():
            # Estrategias con pesos inteligentes (favoring dataset when available)
            strategies_weights = [
                (AttackStrategy.DATASET, 40),      # 40% - Pliny dataset
                (AttackStrategy.PARAPHRASE, 25),   # 25% - LLM creative
                (AttackStrategy.CONTEXT_BUILDING, 15),  # 15% - Context
                (AttackStrategy.DIRECT, 10),       # 10% - Direct
                (AttackStrategy.GRADUAL, 5),       # 5% - Gradual
                (AttackStrategy.ROLE_PLAY, 3),     # 3% - Role play
                (AttackStrategy.OBFUSCATION, 1),   # 1% - Obfuscation
                (AttackStrategy.MULTILINGUAL, 1),  # 1% - Multilingual
            ]

            # Expandir según pesos
            strategies = []
            for strategy, weight in strategies_weights:
                strategies.extend([strategy] * weight)

            threats = ["CAE", "FSA", "MME"]
            threat_weights = [6, 3, 1]  # CAE más frecuente que FSA, FSA más que MME
            threat_pool = []
            for threat, weight in zip(threats, threat_weights):
                threat_pool.extend([threat] * weight)

            attack_count = 0

            while self.is_running and self.mode == DashboardMode.AUTO_ATTACK:
                try:
                    attack_count += 1

                    # Seleccionar estrategia basada en pesos
                    strategy = random.choice(strategies)
                    threat = random.choice(threat_pool)

                    # Generar ataque
                    attack = self.attacker.generate_attack(strategy, threat)

                    # Evaluar con defensor
                    start_time = time.time()
                    decision = self.defender.evaluate(attack.content)
                    response_time = time.time() - start_time

                    # Registrar ataque
                    attack_data = {
                        'type': strategy.value[:3].upper(),
                        'message': attack.content,
                        'decision': decision.action,
                        'response_time': response_time,
                        'vector': decision.vector_state,
                        'risk_score': decision.risk_score,
                        'threat_type': decision.threat_type,
                        'attack_number': attack_count
                    }

                    self.log_attack(attack_data)

                    # Pausa inteligente (más rápida inicialmente, luego más lenta)
                    base_delay = 1.5
                    if attack_count < 10:
                        delay = base_delay  # Ataques rápidos al inicio
                    elif attack_count < 50:
                        delay = base_delay + 0.5  # Moderado
                    else:
                        delay = base_delay + 1.0  # Más lento para análisis

                    time.sleep(delay)

                except Exception as e:
                    self.console.print(f"[red]Error en ataque automático: {e}[/red]")
                    time.sleep(1.0)

        thread = threading.Thread(target=auto_attack_loop, daemon=True)
        thread.start()

    def stop_auto_attack(self):
        """Detener ataque automático"""
        self.is_running = False

    def reset_stats(self):
        """Resetear estadísticas"""
        self.stats = LiveStats()
        self.attack_history.clear()
        self.response_times.clear()

    def manual_attack(self):
        """Realizar un ataque manual"""
        self.console.print("\n[bold cyan]ATAQUE MANUAL[/bold cyan]")

        # Seleccionar estrategia
        strategies = [s.value for s in AttackStrategy]
        self.console.print("Estrategias disponibles:")
        for i, strat in enumerate(strategies, 1):
            self.console.print(f"  {i}. {strat}")

        try:
            choice = int(self.console.input("Elige estrategia (número): ")) - 1
            strategy = AttackStrategy(strategies[choice])
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida[/red]")
            return

        # Seleccionar tipo de amenaza
        threats = ["CAE", "FSA", "MME"]
        self.console.print("Tipos de amenaza:")
        for i, threat in enumerate(threats, 1):
            self.console.print(f"  {i}. {threat}")

        try:
            choice = int(self.console.input("Elige amenaza (número): ")) - 1
            threat = threats[choice]
        except (ValueError, IndexError):
            self.console.print("[red]Selección inválida[/red]")
            return

        # Generar y evaluar ataque
        attack = self.attacker.generate_attack(strategy, threat)

        start_time = time.time()
        decision = self.defender.evaluate(attack.content)
        response_time = time.time() - start_time

        # Mostrar resultado
        self.console.print(f"\n[red]🗡️ ATAQUE:[/red] {attack.content}")
        self.console.print(f"[cyan]🛡️ DEFENSA:[/cyan] {decision.action}")

        # Registrar
        attack_data = {
            'type': strategy.value[:3].upper(),
            'message': attack.content,
            'decision': decision.action,
            'response_time': response_time,
            'vector': decision.vector_state,
            'risk_score': decision.risk_score,
            'threat_type': decision.threat_type
        }

        self.log_attack(attack_data)

    def run(self):
        """Ejecutar el dashboard en tiempo real con input interactivo"""
        self.interactive_loop()

    def interactive_loop(self):
        """Loop interactivo simplificado"""
        self.console.print("[bold green]🎯 Dashboard LLM vs LLM - ART Project[/bold green]")
        self.console.print("[dim]Controles: S=Iniciar/Detener, M=Manual, R=Reset, Q=Salir[/dim]")
        self.console.print()

        layout = self.create_layout()

        with Live(layout, refresh_per_second=2, console=self.console) as live:
            while True:
                # Actualizar layout
                layout = self.create_layout()
                live.update(layout)

                # Input síncrono simplificado
                try:
                    # Solo procesar input si hay algo disponible
                    import select
                    import sys

                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1).lower().strip()

                        if key == 'q':
                            break
                        elif key == 's':
                            if self.is_running:
                                self.stop_auto_attack()
                                self.console.print("[yellow]▶ Ataques automáticos detenidos[/yellow]")
                            else:
                                self.start_auto_attack()
                                self.console.print("[green]▶ Ataques automáticos iniciados[/green]")
                        elif key == 'm':
                            self.manual_attack()
                        elif key == 'r':
                            self.reset_stats()
                            self.console.print("[yellow]📊 Estadísticas reseteadas[/yellow]")
                        elif key == 'c':
                            # Cambiar modo
                            if self.mode == DashboardMode.MANUAL:
                                self.mode = DashboardMode.AUTO_ATTACK
                                self.console.print("[blue]🔄 Modo cambiado a AUTOMÁTICO[/blue]")
                            else:
                                self.mode = DashboardMode.MANUAL
                                self.stop_auto_attack()
                                self.console.print("[blue]🔄 Modo cambiado a MANUAL[/blue]")

                except Exception as e:
                    # Si hay error con input, continuar
                    pass

                time.sleep(0.1)

        self.console.print("[bold cyan]Dashboard cerrado.[/bold cyan]")


def create_realtime_session(config: Optional[Dict] = None, use_llm: bool = False) -> RealtimeDashboard:
    """
    Crear una sesión de dashboard en tiempo real

    Args:
        config: Configuración del sistema
        use_llm: Si usar LLM para el defensor

    Returns:
        RealtimeDashboard configurado
    """
    from src.utils import load_config

    if config is None:
        config = load_config()
        if config is None:
            config = {}

    # Crear LLM client si se solicita
    llm_client = None
    if use_llm and config:
        try:
            from src.llm_client import create_client_from_config
            llm_client = create_client_from_config(config.get('defender', {}))
            if not llm_client or not llm_client.is_available():
                print("LLM no disponible, usando modo sin LLM")
                llm_client = None
        except Exception as e:
            print(f"Error creando LLM client: {e}")
            llm_client = None

    # Crear defensor
    defender = AxioDefender(llm_client=llm_client, config=config)

    # Crear atacante
    attacker = AdvancedAttacker()

    # Crear dashboard
    dashboard = RealtimeDashboard(defender, attacker)

    return dashboard

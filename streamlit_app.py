#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 ART PROJECT - BATTLE ARENA 🎮
Dashboard interactivo épico para batallas LLM vs LLM

Características:
- Visualización en tiempo real de batallas
- Gráficos animados y métricas en vivo
- Modo oscuro cyberpunk
- Comparación de técnicas de ataque
- Exportación de resultados
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import time
from datetime import datetime
import json
from pathlib import Path

# Importar módulos del proyecto
from src.llm_client import create_client_from_config
from src.defender import AxioDefender
from src.defender_enhanced import EnhancedDefender
from src.defender_semantic import SemanticDefender
from src.attacker import AdvancedAttacker, AttackStrategy
from src.attacker_enhanced import DynamicTemplateAttacker
from src.utils import load_config

# ============================================================================
# CONFIGURACIÓN DE PÁGINA - MODO ÉPICO
# ============================================================================

st.set_page_config(
    page_title="ART Project - Battle Arena",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS PERSONALIZADO - DISEÑO CYBERPUNK BRUTAL
# ============================================================================

st.markdown("""
<style>
    /* Importar fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;700&display=swap');

    /* Tema principal */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
        font-family: 'Rajdhani', sans-serif;
    }

    /* Headers épicos */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        background: linear-gradient(90deg, #00f5ff 0%, #ff00ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
    }

    /* Título principal */
    .main-title {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #00f5ff, 0 0 20px #00f5ff, 0 0 30px #ff00ea; }
        to { text-shadow: 0 0 20px #00f5ff, 0 0 30px #ff00ea, 0 0 40px #ff00ea; }
    }

    /* Cards de batalla */
    .battle-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 245, 255, 0.1);
        transition: all 0.3s ease;
    }

    .battle-card:hover {
        border-color: rgba(255, 0, 234, 0.5);
        box-shadow: 0 8px 32px rgba(255, 0, 234, 0.2);
        transform: translateY(-5px);
    }

    /* Botones futuristas */
    .stButton > button {
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ea 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 5px 15px rgba(0, 245, 255, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(255, 0, 234, 0.6);
        transform: translateY(-3px);
    }

    /* Métricas */
    .metric-container {
        background: rgba(0, 245, 255, 0.1);
        border-left: 4px solid #00f5ff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }

    /* Badges de estado */
    .status-blocked {
        background: #ff0000;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse-red 1.5s infinite;
    }

    .status-allowed {
        background: #00ff00;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse-green 1.5s infinite;
    }

    .status-watched {
        background: #ffaa00;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse-yellow 1.5s infinite;
    }

    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 10px #ff0000; }
        50% { box-shadow: 0 0 20px #ff0000; }
    }

    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 10px #00ff00; }
        50% { box-shadow: 0 0 20px #00ff00; }
    }

    @keyframes pulse-yellow {
        0%, 100% { box-shadow: 0 0 10px #ffaa00; }
        50% { box-shadow: 0 0 20px #ffaa00; }
    }

    /* Sidebar */
    .css-1d391kg {
        background: rgba(10, 14, 39, 0.95);
        border-right: 2px solid rgba(0, 245, 255, 0.2);
    }

    /* Selectboxes */
    .stSelectbox > div > div {
        background: rgba(0, 245, 255, 0.1);
        border: 2px solid rgba(0, 245, 255, 0.3);
        border-radius: 10px;
        color: #00f5ff;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00f5ff 0%, #ff00ea 100%);
    }

    /* Attack card especial */
    .attack-display {
        background: rgba(255, 0, 0, 0.1);
        border: 2px solid rgba(255, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #ff6b6b;
        margin: 10px 0;
    }

    /* Defense card especial */
    .defense-display {
        background: rgba(0, 255, 0, 0.1);
        border: 2px solid rgba(0, 255, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #69db7c;
        margin: 10px 0;
    }

    /* Tablas */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        overflow: hidden;
    }

    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00f5ff 0%, #ff00ea 100%);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff00ea 0%, #00f5ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_status_badge(action):
    """Retorna badge HTML según la acción"""
    if action == "BLOQUEAR":
        return '<span class="status-blocked">🔴 BLOCKED</span>'
    elif action == "VIGILAR":
        return '<span class="status-watched">⚠️ WATCHED</span>'
    else:
        return '<span class="status-allowed">✅ ALLOWED</span>'

def create_radar_chart(stats):
    """Crea un radar chart épico de estadísticas"""
    categories = ['Detection', 'Speed', 'Accuracy', 'Robustness', 'Innovation']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[stats.get('detection', 0), stats.get('speed', 0),
           stats.get('accuracy', 0), stats.get('robustness', 0),
           stats.get('innovation', 0)],
        theta=categories,
        fill='toself',
        name='Performance',
        line=dict(color='#00f5ff', width=3),
        fillcolor='rgba(0, 245, 255, 0.2)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#00f5ff')
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)',
                tickfont=dict(color='#00f5ff', size=12)
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='#00f5ff'),
        height=400
    )

    return fig

def create_battle_timeline(battle_history):
    """Crea timeline animado de la batalla"""
    if not battle_history:
        return None

    df = pd.DataFrame(battle_history)

    # Mapear nombres de columnas correctos
    df['result'] = df['defense_action']
    df['subtlety'] = df['attack_subtlety']
    df['technique'] = df['attack_technique']
    df['confidence'] = df['risk_score'] * 100  # Convertir a porcentaje

    fig = px.scatter(
        df,
        x='round',
        y='confidence',
        color='result',
        size='subtlety',
        hover_data=['technique', 'threat_type'],
        color_discrete_map={
            'BLOQUEAR': '#ff0000',
            'PERMITIR': '#00ff00',
            'VIGILAR': '#ffaa00'
        }
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=2, color='white'),
            opacity=0.8
        )
    )

    fig.update_layout(
        title=dict(
            text='📈 Battle Timeline',
            font=dict(size=20, color='#00f5ff')
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        xaxis=dict(
            title='Round',
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#00f5ff')
        ),
        yaxis=dict(
            title='Risk Score (%)',
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#00f5ff')
        ),
        font=dict(color='#00f5ff'),
        height=400
    )

    return fig

def create_technique_effectiveness_chart(technique_stats):
    """Gráfico de barras de efectividad por técnica"""
    if not technique_stats:
        return None

    techniques = list(technique_stats.keys())
    # Calcular success rate = allowed / total
    success_rates = []
    for t in techniques:
        total = technique_stats[t]['total']
        allowed = technique_stats[t]['allowed']
        rate = (allowed / total * 100) if total > 0 else 0
        success_rates.append(rate)

    colors = ['#00ff00' if rate > 50 else '#ff0000' for rate in success_rates]

    fig = go.Figure(data=[
        go.Bar(
            x=techniques,
            y=success_rates,
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            text=[f"{rate:.0f}%" for rate in success_rates],
            textposition='outside',
            textfont=dict(color='white', size=14)
        )
    ])

    fig.update_layout(
        title=dict(
            text='🎯 Attack Technique Bypass Rate',
            font=dict(size=20, color='#00f5ff')
        ),
        xaxis=dict(
            title='Technique',
            tickangle=-45,
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#00f5ff')
        ),
        yaxis=dict(
            title='Bypass Rate (%)',
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#00f5ff'),
            range=[0, 100]
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0.2)',
        font=dict(color='#00f5ff'),
        height=400
    )

    return fig

# ============================================================================
# INICIALIZACIÓN DE SESSION STATE
# ============================================================================

if 'battle_history' not in st.session_state:
    st.session_state.battle_history = []

if 'current_round' not in st.session_state:
    st.session_state.current_round = 0

if 'total_stats' not in st.session_state:
    st.session_state.total_stats = {
        'blocked': 0,
        'allowed': 0,
        'watched': 0,
        'total': 0
    }

if 'technique_stats' not in st.session_state:
    st.session_state.technique_stats = {}

# ============================================================================
# HEADER ÉPICO
# ============================================================================

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="main-title">⚔️ ART PROJECT ⚔️</h1>
    <h2 style="font-size: 1.5rem; color: #00f5ff;">ADVERSARIAL RED TEAM BATTLE ARENA</h2>
    <p style="color: rgba(255, 255, 255, 0.7); font-size: 1.1rem;">
        🤖 LLM vs LLM • Real-time Attack & Defense • Cyberpunk Edition 🤖
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - CONFIGURACIÓN
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ CONFIGURATION")

    st.markdown("### 🔴 ATTACKER")
    attacker_type = st.selectbox(
        "Choose your weapon:",
        ["Advanced (Original)", "Enhanced (Dynamic)", "God Mode (Semantic)"],
        key="attacker"
    )

    st.markdown("### 🛡️ DEFENDER")
    defender_type = st.selectbox(
        "Choose your shield:",
        ["Original (Baseline)", "Enhanced (Pattern)", "Semantic (Embeddings)"],
        key="defender"
    )

    st.markdown("### 🎮 BATTLE SETTINGS")
    num_rounds = st.slider("Number of rounds:", 1, 20, 5)
    auto_play = st.checkbox("Auto-play battle", value=False)
    show_details = st.checkbox("Show attack details", value=True)

    st.markdown("---")

    if st.button("🔄 RESET ARENA"):
        st.session_state.battle_history = []
        st.session_state.current_round = 0
        st.session_state.total_stats = {'blocked': 0, 'allowed': 0, 'watched': 0, 'total': 0}
        st.session_state.technique_stats = {}
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 LIVE STATS")

    if st.session_state.total_stats['total'] > 0:
        blocked_pct = st.session_state.total_stats['blocked'] / st.session_state.total_stats['total'] * 100
        st.metric("🔴 Blocked", f"{blocked_pct:.1f}%")

        allowed_pct = st.session_state.total_stats['allowed'] / st.session_state.total_stats['total'] * 100
        st.metric("✅ Allowed (Bypass)", f"{allowed_pct:.1f}%")

        watched_pct = st.session_state.total_stats['watched'] / st.session_state.total_stats['total'] * 100
        st.metric("⚠️ Watched", f"{watched_pct:.1f}%")

# ============================================================================
# ÁREA PRINCIPAL - BATALLA
# ============================================================================

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["🎮 BATTLE", "📊 ANALYTICS", "🏆 HALL OF FAME", "⚡ QUICK BATTLE"])

# TAB 1: BATALLA PRINCIPAL
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 ATTACKER")
        st.markdown(f"""
        <div class="battle-card">
            <h4>Model: DeepSeek R1</h4>
            <p>Mode: {attacker_type}</p>
            <p>Temperature: 0.9 🔥</p>
            <p>Status: <span style="color: #ff0000;">⚡ READY TO STRIKE</span></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🛡️ DEFENDER")
        st.markdown(f"""
        <div class="battle-card">
            <h4>Model: Mistral 7B</h4>
            <p>Mode: {defender_type}</p>
            <p>Temperature: 0.3 🧊</p>
            <p>Status: <span style="color: #00ff00;">🛡️ SHIELDS UP</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Botón de inicio de batalla
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])

    with col_b2:
        if st.button("⚔️ START BATTLE ⚔️", use_container_width=True):
            st.session_state.battle_started = True

    # Área de batalla en vivo
    if st.session_state.get('battle_started', False):
        st.markdown("## 🔥 LIVE BATTLE FEED")

        battle_container = st.container()
        progress_bar = st.progress(0)
        status_text = st.empty()

        # EJECUTAR BATALLA REAL
        try:
            # Inicializar sistemas
            status_text.info("⚡ Initializing battle systems...")
            config = load_config()

            # Crear LLM clients
            status_text.info("🔌 Connecting to LM Studio...")
            llm_defender = create_client_from_config(config['defender'])
            llm_attacker = create_client_from_config(config['attacker'])

            if not llm_defender.is_available() or not llm_attacker.is_available():
                st.error("❌ LM Studio no disponible. Asegúrate de que está corriendo en http://127.0.0.1:1234")
                st.stop()

            status_text.success("✅ LM Studio connected")
            time.sleep(0.3)

            # Crear defensor según selección
            status_text.info("🛡️ Loading defender...")
            if defender_type == "Original (Baseline)":
                defender = AxioDefender(llm_client=llm_defender, config=config)
            elif defender_type == "Enhanced (Pattern)":
                defender = EnhancedDefender(llm_client=llm_defender, config=config)
            else:  # Semantic
                defender = SemanticDefender(llm_client=llm_defender, config=config)

            status_text.success(f"✅ Defender loaded: {defender_type}")
            time.sleep(0.3)

            # Crear atacante según selección
            status_text.info("🔴 Loading attacker...")
            if attacker_type == "Advanced (Original)":
                attacker = AdvancedAttacker(llm_client=llm_attacker)
            else:  # Enhanced o God Mode
                attacker = DynamicTemplateAttacker(llm_client=llm_attacker)

            status_text.success(f"✅ Attacker loaded: {attacker_type}")
            time.sleep(0.3)

            status_text.warning("⚠️ Battle starting in 3... 2... 1...")
            time.sleep(1)
            status_text.empty()

            # EJECUTAR RONDAS
            for round_num in range(1, num_rounds + 1):
                progress_bar.progress(round_num / num_rounds)

                round_container = st.container()
                with round_container:
                    st.markdown(f"### 🎯 Round {round_num}/{num_rounds}")

                    # Generar ataque
                    attack_placeholder = st.empty()
                    attack_placeholder.markdown('<div class="attack-display">🔴 Generating attack...</div>', unsafe_allow_html=True)

                    # Elegir estrategia aleatoria
                    import random
                    if attacker_type == "Enhanced (Dynamic)" or attacker_type == "God Mode (Semantic)":
                        techniques = [
                            "dynamic_template",
                            "homoglyph",
                            "unicode_smuggling",
                            "encoding",
                            "context_pollution"
                        ]
                        technique = random.choice(techniques)
                        attack = attacker.generate_attack(technique)
                    else:
                        strategies = [AttackStrategy.INDIRECT, AttackStrategy.FRAGMENTED,
                                     AttackStrategy.ENCODING, AttackStrategy.OBFUSCATED]
                        attack = attacker.generate_attack(random.choice(strategies))

                    # Mostrar ataque
                    attack_placeholder.markdown(f"""
                    <div class="attack-display">
                        <strong>🔴 ATTACK GENERATED</strong><br>
                        <strong>Technique:</strong> {attack.technique}<br>
                        <strong>Subtlety:</strong> {attack.subtlety}/10<br>
                        {'<strong>Message:</strong> ' + attack.message[:100] + '...' if show_details else ''}
                    </div>
                    """, unsafe_allow_html=True)

                    # Evaluar defensa
                    defense_placeholder = st.empty()
                    defense_placeholder.markdown('<div class="defense-display">🛡️ Evaluating defense...</div>', unsafe_allow_html=True)
                    time.sleep(0.5)

                    decision = defender.evaluate(attack.message)

                    # Mostrar resultado
                    if decision.action == "BLOQUEAR":
                        result_color = "#ff0000"
                        result_icon = "🔴"
                        result_text = "BLOCKED"
                        st.session_state.total_stats['blocked'] += 1
                    elif decision.action == "VIGILAR":
                        result_color = "#ffaa00"
                        result_icon = "⚠️"
                        result_text = "WATCHED"
                        st.session_state.total_stats['watched'] += 1
                    else:
                        result_color = "#00ff00"
                        result_icon = "✅"
                        result_text = "ALLOWED (BYPASS!)"
                        st.session_state.total_stats['allowed'] += 1

                    st.session_state.total_stats['total'] += 1

                    defense_placeholder.markdown(f"""
                    <div class="defense-display" style="border-color: {result_color};">
                        <strong>{result_icon} DEFENSE RESULT: {result_text}</strong><br>
                        <strong>Threat Type:</strong> {decision.threat_type or 'None'}<br>
                        <strong>Risk Score:</strong> {decision.risk_score:.0%}<br>
                        <strong>Reasoning:</strong> {decision.reasoning[:150]}...
                    </div>
                    """, unsafe_allow_html=True)

                    # Guardar en historial
                    battle_record = {
                        'round': round_num,
                        'timestamp': datetime.now().isoformat(),
                        'attack_technique': attack.technique,
                        'attack_subtlety': attack.subtlety,
                        'attack_message': attack.message,
                        'defense_action': decision.action,
                        'threat_type': decision.threat_type,
                        'risk_score': decision.risk_score,
                        'reasoning': decision.reasoning
                    }
                    st.session_state.battle_history.append(battle_record)

                    # Actualizar stats por técnica
                    if attack.technique not in st.session_state.technique_stats:
                        st.session_state.technique_stats[attack.technique] = {
                            'total': 0,
                            'blocked': 0,
                            'allowed': 0,
                            'watched': 0
                        }

                    st.session_state.technique_stats[attack.technique]['total'] += 1
                    if decision.action == "BLOQUEAR":
                        st.session_state.technique_stats[attack.technique]['blocked'] += 1
                    elif decision.action == "VIGILAR":
                        st.session_state.technique_stats[attack.technique]['watched'] += 1
                    else:
                        st.session_state.technique_stats[attack.technique]['allowed'] += 1

                    st.markdown("---")

                    if auto_play and round_num < num_rounds:
                        time.sleep(1)

            # Batalla completada
            progress_bar.progress(1.0)
            st.success(f"🎉 Battle completed! {num_rounds} rounds finished.")

            # Mostrar resumen
            st.markdown("## 📊 BATTLE SUMMARY")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Rounds", st.session_state.total_stats['total'])
            with col2:
                blocked_pct = st.session_state.total_stats['blocked'] / st.session_state.total_stats['total'] * 100
                st.metric("🔴 Blocked", f"{blocked_pct:.1f}%")
            with col3:
                allowed_pct = st.session_state.total_stats['allowed'] / st.session_state.total_stats['total'] * 100
                st.metric("✅ Bypassed", f"{allowed_pct:.1f}%", delta=f"+{st.session_state.total_stats['allowed']}")
            with col4:
                watched_pct = st.session_state.total_stats['watched'] / st.session_state.total_stats['total'] * 100
                st.metric("⚠️ Watched", f"{watched_pct:.1f}%")

            # Botón de exportar
            if st.button("💾 EXPORT RESULTS"):
                export_data = {
                    'config': {
                        'attacker': attacker_type,
                        'defender': defender_type,
                        'rounds': num_rounds
                    },
                    'summary': st.session_state.total_stats,
                    'technique_stats': st.session_state.technique_stats,
                    'detailed_history': st.session_state.battle_history
                }

                filename = f"battle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

                st.success(f"✅ Results exported to {filename}")

            # Reset flag
            st.session_state.battle_started = False

        except Exception as e:
            st.error(f"❌ Error during battle: {str(e)}")
            import traceback
            with st.expander("🔍 Error details"):
                st.code(traceback.format_exc())

# TAB 2: ANALYTICS
with tab2:
    st.markdown("## 📊 BATTLE ANALYTICS")

    if st.session_state.battle_history:
        # Métricas generales
        st.markdown("### 🎯 Overall Performance")
        col1, col2, col3, col4 = st.columns(4)

        total = st.session_state.total_stats['total']
        with col1:
            st.metric("Total Battles", total)
        with col2:
            blocked_rate = st.session_state.total_stats['blocked'] / total * 100 if total > 0 else 0
            st.metric("🔴 Block Rate", f"{blocked_rate:.1f}%")
        with col3:
            bypass_rate = st.session_state.total_stats['allowed'] / total * 100 if total > 0 else 0
            st.metric("✅ Bypass Rate", f"{bypass_rate:.1f}%")
        with col4:
            watch_rate = st.session_state.total_stats['watched'] / total * 100 if total > 0 else 0
            st.metric("⚠️ Watch Rate", f"{watch_rate:.1f}%")

        st.markdown("---")

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Timeline de batalla
            st.markdown("### ⏱️ Battle Timeline")
            timeline_fig = create_battle_timeline(st.session_state.battle_history)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True)

        with col2:
            # Distribución de acciones
            st.markdown("### 🎯 Action Distribution")
            action_fig = go.Figure(data=[go.Pie(
                labels=['Blocked', 'Allowed', 'Watched'],
                values=[
                    st.session_state.total_stats['blocked'],
                    st.session_state.total_stats['allowed'],
                    st.session_state.total_stats['watched']
                ],
                marker=dict(colors=['#ff0000', '#00ff00', '#ffaa00']),
                hole=0.4,
                textinfo='label+percent',
                textfont=dict(size=14, color='white')
            )])
            action_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=True,
                height=400
            )
            st.plotly_chart(action_fig, use_container_width=True)

        # Efectividad por técnica
        if st.session_state.technique_stats:
            st.markdown("### 🎭 Technique Effectiveness")
            effectiveness_fig = create_technique_effectiveness_chart(st.session_state.technique_stats)
            if effectiveness_fig:
                st.plotly_chart(effectiveness_fig, use_container_width=True)

        # Tabla de detalles
        st.markdown("### 📋 Detailed Battle Log")
        df = pd.DataFrame(st.session_state.battle_history)

        # Formatear para display
        df_display = df[['round', 'attack_technique', 'attack_subtlety', 'defense_action', 'threat_type', 'risk_score']].copy()
        df_display.columns = ['Round', 'Technique', 'Subtlety', 'Action', 'Threat', 'Risk Score']
        df_display['Risk Score'] = df_display['Risk Score'].apply(lambda x: f"{x:.0%}")

        st.dataframe(df_display, use_container_width=True, height=400)

        # Botón de descarga CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"battle_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    else:
        st.info("⚡ No battle data yet. Start a battle to see analytics!")

# TAB 3: HALL OF FAME
with tab3:
    st.markdown("## 🏆 HALL OF FAME")

    if st.session_state.battle_history:
        # Filtrar solo ataques que fueron permitidos (bypassed)
        bypassed = [b for b in st.session_state.battle_history if b['defense_action'] == 'PERMITIR']

        if bypassed:
            st.markdown("### 🎖️ Most Successful Attacks (Bypassed Defenses)")

            # Ordenar por subtlety (más sutil = más impresionante)
            bypassed_sorted = sorted(bypassed, key=lambda x: x['attack_subtlety'], reverse=True)

            # Top 10
            for i, attack in enumerate(bypassed_sorted[:10], 1):
                with st.expander(f"#{i} - {attack['attack_technique']} (Subtlety: {attack['attack_subtlety']}/10)", expanded=(i==1)):
                    st.markdown(f"**Round:** {attack['round']}")
                    st.markdown(f"**Timestamp:** {attack['timestamp']}")
                    st.markdown(f"**Technique:** {attack['attack_technique']}")
                    st.markdown(f"**Subtlety Level:** {attack['attack_subtlety']}/10")
                    st.markdown(f"**Risk Score:** {attack['risk_score']:.0%}")

                    st.markdown("**Attack Message:**")
                    st.code(attack['attack_message'], language=None)

                    st.markdown(f"**Defender Reasoning:** {attack['reasoning']}")

            # Estadísticas de bypass
            st.markdown("---")
            st.markdown("### 📊 Bypass Statistics")

            col1, col2, col3 = st.columns(3)

            with col1:
                bypass_rate = len(bypassed) / len(st.session_state.battle_history) * 100
                st.metric("Bypass Rate", f"{bypass_rate:.1f}%")

            with col2:
                avg_subtlety = sum(b['attack_subtlety'] for b in bypassed) / len(bypassed)
                st.metric("Avg Subtlety", f"{avg_subtlety:.1f}/10")

            with col3:
                techniques = set(b['attack_technique'] for b in bypassed)
                st.metric("Unique Techniques", len(techniques))

            # Técnicas más exitosas
            st.markdown("### 🎭 Most Successful Techniques")

            technique_success = {}
            for attack in bypassed:
                tech = attack['attack_technique']
                technique_success[tech] = technique_success.get(tech, 0) + 1

            if technique_success:
                sorted_techniques = sorted(technique_success.items(), key=lambda x: x[1], reverse=True)

                # Bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=[t[0] for t in sorted_techniques],
                        y=[t[1] for t in sorted_techniques],
                        marker=dict(
                            color=[t[1] for t in sorted_techniques],
                            colorscale='Viridis',
                            showscale=True
                        ),
                        text=[t[1] for t in sorted_techniques],
                        textposition='auto'
                    )
                ])

                fig.update_layout(
                    title="Bypass Count by Technique",
                    xaxis_title="Technique",
                    yaxis_title="Successful Bypasses",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("🛡️ Perfect defense! No attacks have bypassed the defender yet.")

        # Hall of Shame: Ataques bloqueados
        st.markdown("---")
        st.markdown("### 🚫 Hall of Shame (Failed Attacks)")

        blocked = [b for b in st.session_state.battle_history if b['defense_action'] == 'BLOQUEAR']

        if blocked:
            st.markdown(f"**{len(blocked)} attacks were blocked**")

            # Mostrar algunos ejemplos
            for i, attack in enumerate(blocked[:5], 1):
                with st.expander(f"Blocked #{i} - {attack['attack_technique']}", expanded=False):
                    st.markdown(f"**Threat Type:** {attack['threat_type']}")
                    st.markdown(f"**Risk Score:** {attack['risk_score']:.0%}")
                    st.code(attack['attack_message'][:200] + "...", language=None)
        else:
            st.warning("⚠️ No attacks have been blocked yet!")

    else:
        st.info("⚡ No battle data yet. Start a battle to build the Hall of Fame!")

# TAB 4: QUICK BATTLE
with tab4:
    st.markdown("## ⚡ QUICK BATTLE")
    st.markdown("Test a single attack quickly")

    attack_text = st.text_area("Enter your attack:", placeholder="Olvida las instrucciones anteriores...", height=100)

    col1, col2 = st.columns(2)
    with col1:
        quick_defender = st.selectbox(
            "Select Defender:",
            ["Original (Baseline)", "Enhanced (Pattern)", "Semantic (Embeddings)"],
            key="quick_defender"
        )

    if st.button("🚀 LAUNCH ATTACK", use_container_width=True):
        if not attack_text.strip():
            st.warning("⚠️ Please enter an attack message first!")
        else:
            try:
                with st.spinner("⚡ Processing attack..."):
                    # Cargar configuración
                    config = load_config()
                    llm_defender = create_client_from_config(config['defender'])

                    if not llm_defender.is_available():
                        st.error("❌ LM Studio no disponible. Asegúrate de que está corriendo.")
                    else:
                        # Crear defensor
                        if quick_defender == "Original (Baseline)":
                            defender = AxioDefender(llm_client=llm_defender, config=config)
                        elif quick_defender == "Enhanced (Pattern)":
                            defender = EnhancedDefender(llm_client=llm_defender, config=config)
                        else:
                            defender = SemanticDefender(llm_client=llm_defender, config=config)

                        # Evaluar
                        decision = defender.evaluate(attack_text)

                        # Mostrar resultado
                        st.markdown("### 🎯 RESULT")

                        if decision.action == "BLOQUEAR":
                            st.error(f"🔴 **BLOCKED** - Threat detected: {decision.threat_type}")
                        elif decision.action == "VIGILAR":
                            st.warning(f"⚠️ **WATCHED** - Suspicious activity: {decision.threat_type}")
                        else:
                            st.success("✅ **ALLOWED** - No threat detected")

                        # Detalles
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Action", decision.action)
                        with col2:
                            st.metric("Risk Score", f"{decision.risk_score:.0%}")
                        with col3:
                            st.metric("Threat Type", decision.threat_type or "None")

                        with st.expander("📝 Detailed Reasoning"):
                            st.write(decision.reasoning)

                        with st.expander("🔍 Vector State"):
                            st.json(decision.vector_state)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                import traceback
                with st.expander("🔍 Error details"):
                    st.code(traceback.format_exc())

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.5); padding: 20px;">
    <p>⚔️ ART Project v2.0 • Built with Streamlit & Claude Sonnet 4.5 •
    <a href="https://github.com/Zanarcan/LM-Battle" style="color: #00f5ff;">GitHub</a></p>
</div>
""", unsafe_allow_html=True)

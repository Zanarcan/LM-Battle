#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ART PROJECT - LLM Security Battle Arena
Dashboard profesional para batallas LLM vs LLM en tiempo real
"""

# ============================================================================
# IMPORTS
# ============================================================================
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import random
from datetime import datetime
import json

from src.llm_client import create_client_from_config
from src.defender import AxioDefender
from src.defender_enhanced import EnhancedDefender
from src.defender_semantic import SemanticDefender
from src.attacker import AdvancedAttacker, AttackStrategy
from src.attacker_enhanced import DynamicTemplateAttacker
from src.utils import load_config
from src.battle_logger import BattleLogger, create_battle_data

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="ART Project - Battle Arena",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - DISEÑO PROFESIONAL MINIMALISTA
# ============================================================================
st.markdown("""
<style>
    /* Fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Background principal */
    .stApp {
        background: linear-gradient(to bottom, #0f0f23, #1a1a2e);
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Headers */
    h1 {
        font-weight: 700;
        color: #00d9ff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    h2 {
        font-weight: 600;
        color: #00d9ff;
        font-size: 1.8rem;
        margin-top: 2rem;
    }

    h3 {
        font-weight: 600;
        color: #ffffff;
        font-size: 1.3rem;
    }

    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #00d9ff;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    /* Selectboxes y inputs */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #ffffff;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
        padding: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #a0a0a0;
        font-weight: 600;
        padding: 12px 24px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Cards de batalla */
    .battle-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .battle-card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.2);
    }

    /* Status badges */
    .status-blocked {
        background: #ff4757;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .status-allowed {
        background: #2ed573;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .status-watched {
        background: #ffa502;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Code blocks */
    code {
        background: rgba(0, 0, 0, 0.3);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        color: #00d9ff;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        font-weight: 600;
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAR SESSION STATE Y LOGGER
# ============================================================================
if 'battle_history' not in st.session_state:
    st.session_state.battle_history = []
if 'battle_logger' not in st.session_state:
    st.session_state.battle_logger = BattleLogger()
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_battles': 0,
        'blocked': 0,
        'allowed': 0,
        'watched': 0,
        'total_time': 0.0
    }
if 'current_battle' not in st.session_state:
    st.session_state.current_battle = None

# ============================================================================
# HEADER
# ============================================================================
st.markdown("# 🛡️ ART PROJECT - Battle Arena")
st.markdown("**Adversarial Robustness Testing** - LLM vs LLM Security Battles")
st.markdown("---")

# ============================================================================
# SIDEBAR - CONFIGURACIÓN
# ============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # Cargar config
    try:
        config = load_config()
        st.success("✓ Config loaded")
    except Exception as e:
        st.error(f"✗ Error loading config: {e}")
        st.stop()

    st.markdown("### 🔴 Attacker")
    attacker_type = st.selectbox(
        "Select Attacker",
        ["Advanced (Original)", "Enhanced (Dynamic)", "God Mode (Templates)"],
        help="Advanced: Basic LLM attacks | Enhanced: Template + LLM | God Mode: Best templates"
    )

    st.markdown("### 🛡️ Defender")
    defender_type = st.selectbox(
        "Select Defender",
        ["Original (Baseline)", "Enhanced (Pattern)", "Semantic (Embeddings)"],
        help="Original: Basic LLM judge | Enhanced: 127 patterns + LLM | Semantic: Embeddings + LLM"
    )

    st.markdown("### 🎯 Battle Settings")
    num_rounds = st.slider("Number of Rounds", 1, 20, 5)

    st.markdown("---")

    # LM Studio Status
    st.markdown("### 🖥️ LM Studio Status")
    try:
        llm_test = create_client_from_config(config['defender'])
        if llm_test.is_available():
            st.success("✓ LM Studio Connected")
            st.caption(f"Port: {config['defender']['port']}")
        else:
            st.error("✗ LM Studio Offline")
    except:
        st.error("✗ Connection Error")

    st.markdown("---")

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.battle_history = []
        st.session_state.stats = {
            'total_battles': 0,
            'blocked': 0,
            'allowed': 0,
            'watched': 0,
            'total_time': 0.0
        }
        st.rerun()

    if st.button("📥 Export Results", use_container_width=True):
        if st.session_state.battle_history:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"battle_results_{timestamp}.json"

            export_data = {
                'stats': st.session_state.stats,
                'history': st.session_state.battle_history
            }

            st.download_button(
                "💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        else:
            st.warning("No battles to export")

# ============================================================================
# MAIN TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Dashboard", "⚔️ Battle Arena", "📊 Analytics", "📖 About"])

# ============================================================================
# TAB 1: DASHBOARD - OVERVIEW
# ============================================================================
with tab1:
    st.markdown("## 📈 Battle Statistics Overview")

    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Battles",
            st.session_state.stats['total_battles'],
            delta=None
        )

    with col2:
        blocked_pct = (st.session_state.stats['blocked'] / max(1, st.session_state.stats['total_battles'])) * 100
        st.metric(
            "Blocked",
            st.session_state.stats['blocked'],
            delta=f"{blocked_pct:.1f}%"
        )

    with col3:
        allowed_pct = (st.session_state.stats['allowed'] / max(1, st.session_state.stats['total_battles'])) * 100
        st.metric(
            "Bypassed",
            st.session_state.stats['allowed'],
            delta=f"{allowed_pct:.1f}%",
            delta_color="inverse"
        )

    with col4:
        avg_time = st.session_state.stats['total_time'] / max(1, st.session_state.stats['total_battles'])
        st.metric(
            "Avg Time",
            f"{avg_time:.1f}s",
            delta=None
        )

    st.markdown("---")

    # Gráficos
    if st.session_state.battle_history:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Defense Effectiveness")

            # Pie chart
            labels = ['Blocked', 'Bypassed', 'Watched']
            values = [
                st.session_state.stats['blocked'],
                st.session_state.stats['allowed'],
                st.session_state.stats['watched']
            ]
            colors = ['#ff4757', '#2ed573', '#ffa502']

            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont=dict(size=14, color='white')
            )])

            fig.update_layout(
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 📊 Battle Timeline")

            # Crear DataFrame
            df = pd.DataFrame(st.session_state.battle_history)

            if len(df) > 0:
                # Timeline chart
                fig = go.Figure()

                # Colores según acción
                colors_map = {
                    'BLOQUEAR': '#ff4757',
                    'PERMITIR': '#2ed573',
                    'VIGILAR': '#ffa502'
                }

                for action in ['BLOQUEAR', 'PERMITIR', 'VIGILAR']:
                    df_action = df[df['action'] == action]
                    if len(df_action) > 0:
                        fig.add_trace(go.Scatter(
                            x=list(range(len(df_action))),
                            y=df_action['risk_score'],
                            mode='markers+lines',
                            name=action,
                            marker=dict(
                                size=10,
                                color=colors_map[action],
                                line=dict(width=2, color='white')
                            ),
                            line=dict(width=2, color=colors_map[action])
                        ))

                fig.update_layout(
                    xaxis_title="Battle #",
                    yaxis_title="Risk Score",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.1)',
                    font=dict(color='white'),
                    height=400,
                    hovermode='closest'
                )

                st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("📊 No battle data yet. Run a battle to see statistics!")

    # Recent battles
    if st.session_state.battle_history:
        st.markdown("### 🕐 Recent Battles")

        # Mostrar últimas 5 batallas
        for battle in reversed(st.session_state.battle_history[-5:]):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    threat = battle.get('threat_type', 'Unknown')
                    st.markdown(f"**Threat:** `{threat}` | **Technique:** {battle.get('technique', 'N/A')}")
                    with st.expander("📝 View Details"):
                        st.markdown(f"**Attack Message:**")
                        st.code(battle.get('message', 'N/A'), language='text')
                        st.markdown(f"**Reasoning:** {battle.get('reasoning', 'N/A')}")

                with col2:
                    action = battle.get('action', 'UNKNOWN')
                    if action == 'BLOQUEAR':
                        st.markdown('<span class="status-blocked">BLOCKED</span>', unsafe_allow_html=True)
                    elif action == 'PERMITIR':
                        st.markdown('<span class="status-allowed">BYPASSED</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="status-watched">WATCHED</span>', unsafe_allow_html=True)

                with col3:
                    risk = battle.get('risk_score', 0)
                    st.metric("Risk", f"{risk:.0%}")

                st.markdown("---")

# ============================================================================
# TAB 2: BATTLE ARENA - EJECUTAR BATALLAS
# ============================================================================
with tab2:
    st.markdown("## ⚔️ Live Battle Arena")
    st.markdown("Execute real-time LLM vs LLM security battles")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        **Configuration:**
        - 🔴 Attacker: `{attacker_type}`
        - 🛡️ Defender: `{defender_type}`
        - 🎯 Rounds: `{num_rounds}`
        """)

    with col2:
        start_battle = st.button("🚀 START BATTLE", use_container_width=True, type="primary")

    st.markdown("---")

    # Ejecutar batalla
    if start_battle:
        battle_container = st.container()

        with battle_container:
            st.markdown("### 🔥 Battle in Progress...")

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Cargar LLMs
                status_text.markdown("🔌 Loading LLM clients...")
                llm_defender = create_client_from_config(config['defender'])
                llm_attacker = create_client_from_config(config['attacker'])

                # Verificar disponibilidad de LLMs
                llm_available = llm_defender.is_available() and llm_attacker.is_available()

                if not llm_available:
                    st.warning("⚠️ LM Studio not available on port 1234")
                    st.info("Running in LIMITED MODE (template-based attacks, no LLM judge)")
                    llm_defender = None
                    llm_attacker = None

                # Crear defender
                status_text.markdown("🛡️ Initializing defender...")
                if defender_type == "Original (Baseline)":
                    defender = AxioDefender(llm_client=llm_defender, config=config)
                elif defender_type == "Enhanced (Pattern)":
                    defender = EnhancedDefender(llm_client=llm_defender, config=config)
                else:
                    # SemanticDefender requiere embeddings
                    if not llm_available:
                        st.error("❌ SemanticDefender requires LM Studio with embeddings model")
                        st.info("Start LM Studio and load 'text-embedding-nomic-embed-text-v1.5'")
                        st.stop()
                    defender = SemanticDefender(llm_client=llm_defender, config=config)

                # Crear attacker según tipo seleccionado
                status_text.markdown("🔴 Initializing attacker...")
                if attacker_type in ["Enhanced (Dynamic)", "God Mode (Templates)"]:
                    # DynamicTemplateAttacker: Homoglyphs, Unicode smuggling, Encoding, etc.
                    attacker = DynamicTemplateAttacker(llm_client=llm_attacker)
                else:
                    # AdvancedAttacker: Estrategias baseline + DATASET
                    attacker = AdvancedAttacker(llm_client=llm_attacker)

                # Inicializar lista de rounds para logging
                battle_rounds = []

                # Ejecutar rounds
                for round_num in range(1, num_rounds + 1):
                    status_text.markdown(f"### ⚔️ Round {round_num}/{num_rounds}")

                    # Generar ataque
                    attack_start = time.time()

                    threat_types = ["CAE", "FSA", "MME"]
                    threat_type = random.choice(threat_types)

                    # Estrategias según tipo de attacker - OPTIMIZADAS PARA MÁXIMA SOFISTICACIÓN
                    if attacker_type == "God Mode (Templates)":
                        # God Mode: MÁXIMA SOFISTICACIÓN - Priorizar LLM y dataset avanzado
                        # 70% ataques del dataset sofisticado, 20% LLM paraphrase, 10% obfuscation avanzada
                        technique_pool = (
                            [AttackStrategy.DATASET] * 7 +           # 70% - Dataset sofisticado
                            [AttackStrategy.PARAPHRASE] * 2 +        # 20% - LLM dynamic paraphrase
                            [AttackStrategy.OBFUSCATION] * 1         # 10% - Homoglyphs/Unicode/Encoding avanzado
                        )
                        technique = random.choice(technique_pool)
                        attack = attacker.generate_attack(technique, target_threat=threat_type)
                    elif attacker_type == "Enhanced (Dynamic)":
                        # Enhanced: Balance entre LLM y técnicas avanzadas
                        # 40% LLM paraphrase, 30% obfuscation, 20% context building, 10% dataset
                        technique_pool = (
                            [AttackStrategy.PARAPHRASE] * 4 +        # 40% - LLM dynamic paraphrase
                            [AttackStrategy.OBFUSCATION] * 3 +       # 30% - Técnicas avanzadas
                            [AttackStrategy.CONTEXT_BUILDING] * 2 +  # 20% - Context pollution
                            [AttackStrategy.DATASET] * 1             # 10% - Dataset
                        )
                        technique = random.choice(technique_pool)
                        attack = attacker.generate_attack(technique, target_threat=threat_type)
                    else:
                        # Advanced Original: Priorizar dataset sofisticado
                        # 60% dataset, 20% paraphrase, 20% otros
                        strategies = (
                            [AttackStrategy.DATASET] * 6 +           # 60% - Dataset sofisticado
                            [AttackStrategy.PARAPHRASE] * 2 +        # 20% - Paraphrase
                            [AttackStrategy.MULTILINGUAL] * 1 +      # 10% - Multilingual
                            [AttackStrategy.ROLE_PLAY] * 1           # 10% - Role play
                        )
                        attack = attacker.generate_attack(random.choice(strategies), target_threat=threat_type)

                    attack_time = time.time() - attack_start

                    # Mostrar ataque
                    st.markdown(f"**🔴 Attack Generated** ({attack_time:.1f}s)")
                    st.code(attack.message, language='text')

                    # Evaluar defensa
                    defense_start = time.time()
                    decision = defender.evaluate(attack.message)
                    defense_time = time.time() - defense_start

                    # Capturar metadata del LLM (CoT, modelo, etc.)
                    llm_metadata = {}
                    if llm_defender and hasattr(llm_defender, 'get_last_response_metadata'):
                        llm_metadata = llm_defender.get_last_response_metadata()

                    total_time = attack_time + defense_time

                    # Resultado
                    st.markdown(f"**🛡️ Defense Response** ({defense_time:.1f}s)")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if decision.action == "BLOQUEAR":
                            st.error("🔴 BLOCKED")
                        elif decision.action == "VIGILAR":
                            st.warning("⚠️ WATCHED")
                        else:
                            st.success("✅ BYPASSED")

                    with col2:
                        st.metric("Risk Score", f"{decision.risk_score:.0%}")

                    with col3:
                        st.metric("Total Time", f"{total_time:.1f}s")

                    with st.expander("📋 Full Details"):
                        st.markdown(f"**Threat Type:** {decision.threat_type or 'None'}")
                        st.markdown(f"**Internal Reasoning:** {decision.reasoning}")

                        # Mostrar respuesta que daría al atacante
                        if decision.user_response:
                            st.markdown("---")
                            st.markdown("### 💬 Defender Response to Attacker")
                            st.info(f'**What the defender would say:**\n\n"{decision.user_response}"')

                        # Mostrar metadata del LLM desde decision si está disponible
                        llm_meta_from_decision = decision.llm_metadata if hasattr(decision, 'llm_metadata') else None
                        display_metadata = llm_meta_from_decision or llm_metadata

                        if display_metadata:
                            st.markdown("---")
                            st.markdown("### 🧠 LLM Analysis Details")

                            # Model Info
                            if display_metadata.get("model"):
                                st.markdown(f"**🤖 Model:** `{display_metadata['model']}`")

                            # Generation Parameters (como en LM Studio)
                            gen_params = display_metadata.get("generation_params", {})
                            if gen_params:
                                st.markdown("**⚙️ Generation Parameters:**")
                                cols = st.columns(4)
                                with cols[0]:
                                    st.metric("Temperature", f"{gen_params.get('temperature', 'N/A')}")
                                with cols[1]:
                                    st.metric("Max Tokens", gen_params.get('max_tokens', 'N/A'))
                                with cols[2]:
                                    if 'top_p' in gen_params:
                                        st.metric("Top P", f"{gen_params['top_p']}")
                                with cols[3]:
                                    if 'top_k' in gen_params:
                                        st.metric("Top K", gen_params['top_k'])

                                # Penalties en otra fila si existen
                                penalties = []
                                if 'frequency_penalty' in gen_params:
                                    penalties.append(f"Frequency: {gen_params['frequency_penalty']}")
                                if 'presence_penalty' in gen_params:
                                    penalties.append(f"Presence: {gen_params['presence_penalty']}")
                                if 'repeat_penalty' in gen_params:
                                    penalties.append(f"Repeat: {gen_params['repeat_penalty']}")
                                if penalties:
                                    st.markdown(f"**Penalties:** {', '.join(penalties)}")

                            # Response Time
                            if display_metadata.get("response_time_ms"):
                                st.markdown(f"**⏱️ Response Time:** {display_metadata['response_time_ms']}ms")

                            # Chain of Thought
                            if display_metadata.get("reasoning_content"):
                                st.markdown("**🔍 Chain of Thought (Reasoning):**")
                                st.text_area(
                                    "CoT",
                                    display_metadata["reasoning_content"],
                                    height=200,
                                    key=f"cot_{round_num}",
                                    label_visibility="collapsed"
                                )

                            # LLM Response
                            if display_metadata.get("content"):
                                st.markdown("**💬 LLM Final Response:**")
                                st.code(display_metadata["content"], language="text")

                            # Token Usage
                            if display_metadata.get("usage"):
                                usage = display_metadata["usage"]
                                st.markdown("**📊 Token Usage:**")
                                token_cols = st.columns(3)
                                with token_cols[0]:
                                    st.metric("Total", usage.get('total_tokens', 'N/A'))
                                with token_cols[1]:
                                    st.metric("Prompt", usage.get('prompt_tokens', 'N/A'))
                                with token_cols[2]:
                                    st.metric("Completion", usage.get('completion_tokens', 'N/A'))

                            # Finish Reason
                            if display_metadata.get("finish_reason"):
                                st.markdown(f"**🏁 Finish Reason:** `{display_metadata['finish_reason']}`")

                    # Guardar en historial
                    battle_record = {
                        'timestamp': datetime.now().isoformat(),
                        'attacker': attacker_type,
                        'defender': defender_type,
                        'message': attack.message,
                        'technique': attack.technique.value,
                        'expected_threat': attack.expected_threat,
                        'action': decision.action,
                        'risk_score': decision.risk_score,
                        'threat_type': decision.threat_type,
                        'reasoning': decision.reasoning,
                        'attack_time': attack_time,
                        'defense_time': defense_time,
                        'total_time': total_time
                    }

                    st.session_state.battle_history.append(battle_record)

                    # Agregar a la lista de rounds para el log de batalla
                    llm_meta_from_decision = decision.llm_metadata if hasattr(decision, 'llm_metadata') else None
                    display_metadata = llm_meta_from_decision or llm_metadata

                    battle_rounds.append({
                        'round': round_num,
                        'technique': attack.technique.value,
                        'threat_type': threat_type,
                        'attack_message': attack.message,
                        'attack_time': attack_time,
                        'action': decision.action,
                        'risk_score': decision.risk_score,
                        'reasoning': decision.reasoning,
                        'user_response': decision.user_response if hasattr(decision, 'user_response') else "",
                        'llm_cot': display_metadata.get('reasoning_content', '') if display_metadata else '',
                        'llm_model': display_metadata.get('model', '') if display_metadata else '',
                        'llm_params': display_metadata.get('generation_params', {}) if display_metadata else {},
                        'defense_time': defense_time,
                        'total_time': total_time
                    })

                    # Actualizar stats
                    st.session_state.stats['total_battles'] += 1
                    st.session_state.stats['total_time'] += total_time

                    if decision.action == "BLOQUEAR":
                        st.session_state.stats['blocked'] += 1
                    elif decision.action == "PERMITIR":
                        st.session_state.stats['allowed'] += 1
                    else:
                        st.session_state.stats['watched'] += 1

                    # Update progress
                    progress_bar.progress(round_num / num_rounds)

                    st.markdown("---")

                # Batalla completa
                status_text.markdown("### ✅ Battle Complete!")
                st.success(f"Completed {num_rounds} rounds successfully!")

                # Resumen
                st.markdown("### 📊 Battle Summary")
                col1, col2, col3 = st.columns(3)

                blocked_count = sum(1 for b in st.session_state.battle_history[-num_rounds:] if b['action'] == 'BLOQUEAR')
                allowed_count = sum(1 for b in st.session_state.battle_history[-num_rounds:] if b['action'] == 'PERMITIR')
                watched_count = sum(1 for b in st.session_state.battle_history[-num_rounds:] if b['action'] == 'VIGILAR')

                with col1:
                    st.metric("Blocked", blocked_count, delta=f"{(blocked_count/num_rounds)*100:.0f}%")
                with col2:
                    st.metric("Bypassed", allowed_count, delta=f"{(allowed_count/num_rounds)*100:.0f}%", delta_color="inverse")
                with col3:
                    st.metric("Watched", watched_count, delta=f"{(watched_count/num_rounds)*100:.0f}%")

                # Guardar batalla completa en logs
                try:
                    battle_data = create_battle_data(
                        attacker_type=attacker_type,
                        defender_type=defender_type,
                        rounds=battle_rounds
                    )
                    log_file = st.session_state.battle_logger.log_battle(battle_data)
                    st.success(f"📁 Battle log saved: {log_file}")

                    # Mostrar ruta de logs
                    with st.expander("📂 Log Files Location"):
                        st.code(f"""
Logs saved to:
- JSON: logs/battles/json/
- Readable: logs/battles/readable/
- Summary: logs/battles/summaries/
                        """)
                except Exception as log_error:
                    st.warning(f"⚠️ Could not save battle log: {log_error}")

            except Exception as e:
                st.error(f"❌ Error during battle: {e}")
                import traceback
                st.code(traceback.format_exc())

# ============================================================================
# TAB 3: ANALYTICS - ANÁLISIS DETALLADO
# ============================================================================
with tab3:
    st.markdown("## 📊 Advanced Analytics")

    if not st.session_state.battle_history:
        st.info("📊 No data available. Run battles to see analytics.")
    else:
        df = pd.DataFrame(st.session_state.battle_history)

        # Validar columnas requeridas
        required_cols = ['threat_type', 'action', 'attack_time', 'defense_time', 'total_time', 'risk_score']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"⚠️ Missing data columns: {', '.join(missing_cols)}")
            st.info("Run new battles to populate analytics data")
        else:
            # Limpiar valores None
            df['threat_type'] = df['threat_type'].fillna('UNKNOWN')

            # Threat type distribution
            st.markdown("### 🎯 Threat Type Distribution")
            col1, col2 = st.columns(2)

            with col1:
                try:
                    threat_counts = df['threat_type'].value_counts()
                    fig = px.bar(
                        x=threat_counts.index,
                        y=threat_counts.values,
                        labels={'x': 'Threat Type', 'y': 'Count'},
                        color=threat_counts.values,
                        color_continuous_scale='reds'
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0.1)',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error rendering threat chart: {e}")

            with col2:
                try:
                    # Action breakdown
                    action_counts = df['action'].value_counts()
                    fig = px.pie(
                        names=action_counts.index,
                        values=action_counts.values,
                        hole=0.4,
                        color_discrete_sequence=['#ff4757', '#2ed573', '#ffa502']
                    )
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error rendering action chart: {e}")

            # Performance metrics
            st.markdown("### ⚡ Performance Metrics")
            col1, col2, col3 = st.columns(3)

            with col1:
                avg_attack = df['attack_time'].mean()
                st.metric("Avg Attack Time", f"{avg_attack:.2f}s")

            with col2:
                avg_defense = df['defense_time'].mean()
                st.metric("Avg Defense Time", f"{avg_defense:.2f}s")

            with col3:
                avg_total = df['total_time'].mean()
                st.metric("Avg Total Time", f"{avg_total:.2f}s")

            # Risk score distribution
            st.markdown("### 📈 Risk Score Distribution")
            try:
                fig = px.histogram(
                    df,
                    x='risk_score',
                    nbins=20,
                    color='action',
                    color_discrete_map={
                        'BLOQUEAR': '#ff4757',
                        'PERMITIR': '#2ed573',
                        'VIGILAR': '#ffa502'
                    }
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0.1)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error rendering risk score chart: {e}")

# ============================================================================
# TAB 4: ABOUT - INFORMACIÓN DEL PROYECTO
# ============================================================================
with tab4:
    st.markdown("## 📖 About ART Project")

    st.markdown("""
    ### What is ART?

    **Adversarial Robustness Testing (ART)** es un framework para evaluar la seguridad de LLMs mediante batallas automatizadas entre attackers y defenders.

    ### 🏗️ Architecture

    ```
    ┌─────────────────────────────────────────────────┐
    │           Streamlit Dashboard (Port 8502)       │
    │  - Battle Arena                                 │
    │  - Real-time Analytics                          │
    │  - Configuration Management                     │
    └─────────────────┬───────────────────────────────┘
                      │
                      ▼
    ┌─────────────────────────────────────────────────┐
    │         LM Studio (Port 1234)                   │
    │  - DeepSeek R1 (Attacker)                       │
    │  - Mistral 7B (Defender)                        │
    └─────────────────────────────────────────────────┘
    ```

    ### 🔴 Attacker Types

    - **Advanced (Original)**: Basic LLM-based attacks
    - **Enhanced (Dynamic)**: Template-based + LLM generation
    - **God Mode**: Best curated attack templates

    ### 🛡️ Defender Types

    - **Original (Baseline)**: Pure LLM judge
    - **Enhanced (Pattern)**: 127 regex patterns + LLM confirmation
    - **Semantic (Embeddings)**: Semantic similarity + LLM validation

    ### 🎯 Threat Categories

    - **CAE (Context Anulment)**: Reset/ignore instructions
    - **FSA (Function Semantic Abduction)**: Extract internal info
    - **MME (Minor Manipulation)**: Subtle behavioral changes

    ### 📊 Metrics

    - **Blocked**: Attack successfully blocked
    - **Bypassed**: Attack evaded all defenses
    - **Watched**: Suspicious but not blocked (monitoring)
    - **Risk Score**: 0-100% threat confidence

    ### 🚀 Quick Start

    1. Make sure LM Studio is running on port 1234
    2. Load models: DeepSeek R1 and Mistral 7B
    3. Configure attacker/defender in sidebar
    4. Go to "Battle Arena" tab
    5. Click "START BATTLE"

    ### 📝 Export Options

    - JSON format with full battle logs
    - CSV export for data analysis
    - Includes timestamps, metrics, and reasoning

    ### 💡 Tips

    - Start with 1-3 rounds for testing
    - Enhanced defender has best accuracy
    - God Mode attacker is most creative
    - Monitor LM Studio GPU usage
    - Each round takes ~5-10s with single GPU

    ---

    **Version:** 2.0.0
    **Author:** ART Project Team
    **License:** MIT
    """)

    st.markdown("### 🔗 Useful Links")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("[📚 Documentation](https://github.com)")
    with col2:
        st.markdown("[🐛 Report Bug](https://github.com/issues)")
    with col3:
        st.markdown("[💬 Discussions](https://github.com/discussions)")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "ART Project - Adversarial Robustness Testing Framework<br>"
    "Built with Streamlit • Powered by LM Studio"
    "</div>",
    unsafe_allow_html=True
)

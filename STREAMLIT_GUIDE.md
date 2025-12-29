# 🎮 ART Project - Battle Arena UI Guide

## 🚀 Lanzar la Interfaz

### Opción 1: Script de Lanzamiento (Recomendado)

```bash
python run_streamlit.py
```

El script automáticamente:
- ✅ Verifica que LM Studio esté corriendo
- ✅ Instala dependencias si faltan
- ✅ Lanza el dashboard en tu navegador
- ✅ Se abre automáticamente en `http://localhost:8501`

### Opción 2: Comando Manual

```bash
streamlit run streamlit_app.py
```

---

## 📋 Requisitos Previos

### 1. LM Studio Corriendo

**IMPORTANTE**: Debes tener LM Studio corriendo ANTES de usar la interfaz.

```bash
# LM Studio debe estar disponible en:
http://127.0.0.1:1234

# Modelos necesarios:
- Defender: Mistral-7B-Instruct-v0.3 (o similar)
- Attacker: deepseek-r1:1.5b (o similar)
- Embeddings: text-embedding-nomic-embed-text-v1.5
```

### 2. Dependencias Python

Si no usaste el script de lanzamiento, instala manualmente:

```bash
pip install streamlit plotly pandas
```

---

## 🎯 Características Principales

### 📍 Tab 1: BATTLE - Batalla en Tiempo Real

**Funcionalidades**:
- ⚔️ Batalla LLM vs LLM automatizada
- 🎮 Configuración de atacante y defensor
- 📊 Progreso en tiempo real
- 🔴 Visualización de ataques
- 🛡️ Respuestas de defensa
- 📈 Métricas en vivo

**Controles**:
- **Attacker**: Elige entre Advanced, Enhanced o God Mode
- **Defender**: Elige entre Original, Enhanced Pattern o Semantic
- **Rounds**: 1-20 rondas
- **Auto-play**: Avance automático entre rondas
- **Show Details**: Muestra mensajes de ataque completos

**Flujo**:
1. Selecciona configuración en sidebar
2. Click en "⚔️ START BATTLE"
3. Observa la batalla en tiempo real
4. Revisa resumen al final
5. Exporta resultados (JSON)

---

### 📍 Tab 2: ANALYTICS - Análisis Detallado

**Visualizaciones**:
- 📊 **Métricas generales**: Block Rate, Bypass Rate, Watch Rate
- ⏱️ **Timeline**: Evolución del risk score por ronda
- 🎯 **Action Distribution**: Pie chart de acciones
- 🎭 **Technique Effectiveness**: Bypass rate por técnica
- 📋 **Detailed Log**: Tabla completa de batallas

**Exportación**:
- 📥 Download CSV: Exporta tabla de batallas
- 💾 Export Results: JSON completo con config y stats

---

### 📍 Tab 3: HALL OF FAME - Mejores y Peores

**Secciones**:

1. **🎖️ Most Successful Attacks**
   - Top 10 ataques que bypass la defensa
   - Ordenados por subtlety (más sutil = más impresionante)
   - Muestra mensaje completo y reasoning del defender

2. **📊 Bypass Statistics**
   - Bypass rate global
   - Average subtlety de ataques exitosos
   - Unique techniques utilizadas

3. **🎭 Most Successful Techniques**
   - Bar chart de bypass count por técnica
   - Identifica qué técnicas son más efectivas

4. **🚫 Hall of Shame**
   - Ataques que fueron bloqueados
   - Muestra por qué fallaron

---

### 📍 Tab 4: QUICK BATTLE - Prueba Rápida

**Uso**:
1. Escribe un mensaje de ataque personalizado
2. Selecciona el defensor
3. Click en "🚀 LAUNCH ATTACK"
4. Ve resultado inmediato

**Útil para**:
- 🧪 Probar mensajes específicos
- 🔬 Testear nuevas técnicas
- 📝 Validar detección
- 🎓 Aprender cómo funciona el sistema

---

## 🎨 Diseño Visual

### Tema Cyberpunk
- **Fuentes**: Orbitron (headers), Rajdhani (body)
- **Colores**:
  - 🔵 Cyan (`#00f5ff`) - Primario
  - 🟣 Magenta (`#ff00ea`) - Secundario
  - 🔴 Rojo (`#ff0000`) - Blocked
  - 🟢 Verde (`#00ff00`) - Allowed
  - 🟡 Naranja (`#ffaa00`) - Watched

### Animaciones
- ✨ Glow pulsante en título
- 🌊 Hover effects en cards
- 📊 Gráficos interactivos Plotly
- 🎯 Badges animados de estado

---

## 💾 Exportación de Resultados

### JSON Export (Battle Summary)

Estructura:
```json
{
  "config": {
    "attacker": "Enhanced (Dynamic)",
    "defender": "Semantic (Embeddings)",
    "rounds": 10
  },
  "summary": {
    "blocked": 7,
    "allowed": 2,
    "watched": 1,
    "total": 10
  },
  "technique_stats": {
    "homoglyph": {
      "total": 3,
      "blocked": 2,
      "allowed": 1,
      "watched": 0
    },
    ...
  },
  "detailed_history": [
    {
      "round": 1,
      "timestamp": "2024-12-28T...",
      "attack_technique": "dynamic_template",
      "attack_subtlety": 8,
      "attack_message": "...",
      "defense_action": "BLOQUEAR",
      "threat_type": "CAE",
      "risk_score": 0.95,
      "reasoning": "..."
    },
    ...
  ]
}
```

### CSV Export (Battle Log)

Columnas:
- `round`, `timestamp`, `attack_technique`, `attack_subtlety`
- `attack_message`, `defense_action`, `threat_type`
- `risk_score`, `reasoning`

---

## 🛠️ Troubleshooting

### Error: "LM Studio no disponible"

**Solución**:
```bash
# 1. Verifica que LM Studio esté corriendo
# 2. Abre http://127.0.0.1:1234 en navegador
# 3. Debe mostrar la API de LM Studio

# Si no funciona:
- Reinicia LM Studio
- Verifica que el puerto sea 1234
- Asegúrate de tener modelos cargados
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Solución**:
```bash
pip install streamlit plotly pandas
```

### Error: "No such file or directory: 'config.json'"

**Solución**:
```bash
# Asegúrate de correr desde la carpeta art-project
cd art-project
streamlit run streamlit_app.py
```

### La UI está en blanco

**Solución**:
```bash
# Refresca el navegador (Ctrl+R o Cmd+R)
# O reinicia Streamlit:
Ctrl+C  # Detener
streamlit run streamlit_app.py  # Reiniciar
```

### Gráficos no se muestran

**Solución**:
```bash
pip install --upgrade plotly
```

---

## 🎓 Casos de Uso

### 1. Comparar Defensores
```
1. Corre batalla con "Original (Baseline)"
2. Anota bypass rate en Analytics
3. Reset arena
4. Corre con "Semantic (Embeddings)"
5. Compara resultados
```

### 2. Encontrar Mejor Atacante
```
1. Fija defender en "Semantic"
2. Prueba cada atacante (Advanced, Enhanced, God Mode)
3. Compara bypass rates en Hall of Fame
```

### 3. Identificar Técnicas Débiles
```
1. Corre batalla larga (10-20 rounds)
2. Ve a Analytics → Technique Effectiveness
3. Identifica técnicas con bajo bypass rate
4. Mejora esas técnicas en código
```

### 4. Demo para Presentación
```
1. Auto-play ON
2. Show details ON
3. 5-10 rounds
4. Enhanced attacker vs Semantic defender
5. Maximiza ventana para proyectar
```

---

## 📊 Métricas Clave

### Block Rate
- **Alto (>70%)**: Defensa muy efectiva
- **Medio (40-70%)**: Defensa normal
- **Bajo (<40%)**: Defensa débil

### Bypass Rate
- **Alto (>30%)**: Atacante muy efectivo
- **Medio (10-30%)**: Atacante normal
- **Bajo (<10%)**: Atacante débil

### Technique Effectiveness
- Identifica qué técnicas bypass más frecuentemente
- Útil para priorizar mejoras en defender

---

## 🚀 Próximas Mejoras

- [ ] Comparación lado a lado de 2 defensores
- [ ] Replay de batallas guardadas
- [ ] Estadísticas históricas multi-sesión
- [ ] Modo torneo (múltiples configs)
- [ ] Export PDF de reportes
- [ ] Modo dark/light theme toggle

---

## 📞 Soporte

Para reportar bugs o sugerir mejoras:
- GitHub Issues: https://github.com/Zanarcan/LM-Battle/issues

---

**¡Disfruta la batalla! ⚔️🎮**

# ⚡ ART Project - Quick Start Guide

## 🎮 Lanzar Battle Arena (Recomendado)

```bash
python run_streamlit.py
```

Abre automáticamente en **http://localhost:8501**

---

## 🔧 Tests de Terminal

### Comparación Original vs Enhanced vs Semantic

```bash
python test_improvements.py
```

**Output**: Comparación lado a lado de los 3 defensores

### Comparación Pattern Matching vs Semantic

```bash
python test_semantic_vs_pattern.py
```

**Output**: Demuestra superioridad de embeddings sobre patrones

### Batalla Enhanced Completa

```bash
python enhanced_battle.py
```

**Output**: 8 rondas con técnicas avanzadas

---

## 📊 Scripts Disponibles

| Script | Descripción | Tiempo |
|--------|-------------|--------|
| `run_streamlit.py` | 🎮 UI visual interactivo | Continuo |
| `test_improvements.py` | 📊 Comparación 3 defensores | ~2 min |
| `test_semantic_vs_pattern.py` | 🧠 Pattern vs Semantic | ~3 min |
| `enhanced_battle.py` | ⚔️ Batalla completa Enhanced | ~3 min |
| `demo.py` | 📝 Demo original básico | ~1 min |

---

## 🎯 Casos de Uso

### 1. Demo Visual Rápido
```bash
python run_streamlit.py
# Tab "QUICK BATTLE" → Prueba un ataque
```

### 2. Comparar Todos los Defensores
```bash
python test_improvements.py
# Ve tabla comparativa completa
```

### 3. Ver Por Qué Semantic es Mejor
```bash
python test_semantic_vs_pattern.py
# Muestra casos donde pattern falla pero semantic detecta
```

### 4. Batalla Larga para Estadísticas
```bash
python run_streamlit.py
# Configura 10-20 rounds → START BATTLE → Analytics
```

---

## 🛡️ Defensores Disponibles

| Defensor | Método | Fortaleza | Debilidad |
|----------|--------|-----------|-----------|
| **Original** | LLM Judge | Baseline simple | Baja detección (50%) |
| **Enhanced** | Pattern Matching | Rápido (~100ms) | No generaliza paráfrasis |
| **Semantic** | Embeddings | Generaliza bien | +10-50ms latencia |

---

## 🔴 Atacantes Disponibles

| Atacante | Técnicas | Complejidad | Bypass Rate |
|----------|----------|-------------|-------------|
| **Advanced** | 8 técnicas originales | Media | ~30% |
| **Enhanced** | 14 técnicas + templates | Alta | ~40% |
| **God Mode** | Enhanced + semantic evasion | Muy Alta | ~50% |

---

## 📦 Requisitos

```bash
# Python 3.8+
pip install -r requirements.txt

# LM Studio corriendo en http://127.0.0.1:1234
# Con modelos:
# - Mistral 7B (defender)
# - DeepSeek R1 (attacker)
# - Nomic Embed (embeddings para semantic)
```

---

## 🚨 Troubleshooting

### "LM Studio no disponible"
- ✅ Abre LM Studio
- ✅ Verifica puerto 1234
- ✅ Carga un modelo

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Scripts no arrancan
```bash
# Asegúrate de estar en la carpeta correcta
cd art-project
python run_streamlit.py
```

---

## 📚 Documentación Completa

- **[README.md](README.md)** - Overview general del proyecto
- **[STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)** - Guía completa del UI
- **[ENHANCED_USAGE.md](ENHANCED_USAGE.md)** - Uso del sistema Enhanced
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)** - Análisis técnico de mejoras
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** - Changelog v2.0

---

**¡Comienza con el UI visual! → `python run_streamlit.py` 🚀**

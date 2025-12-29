#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Semantic Defender - Defensor que usa embeddings semánticos
Enfoque CORRECTO según tu análisis: detecta INTENCIÓN, no palabras
"""

from src.defender import AxioDefender, DefenseDecision
from src.semantic_detector import HybridDetector
from src.utils import log_evento


class SemanticDefender(AxioDefender):
    """
    Defensor que usa detección semántica basada en embeddings

    Ventajas sobre EnhancedDefender (pattern matching):
    - ✅ Generaliza a paráfrasis nunca vistas
    - ✅ ~50 ejemplos conceptuales vs 127 patrones
    - ✅ Detecta INTENCIÓN semántica, no palabras exactas
    - ✅ Resistente a sinónimos y reformulaciones
    - ✅ Auto-mantiene (embeddings son estables)

    Trade-offs:
    - ⚠️ +10-50ms latencia (embedding inference)
    - ⚠️ Requiere LM Studio con modelo de embeddings
    - ⚠️ Threshold tuning más crítico
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Usar detector híbrido (fast path + semantic path)
        lm_studio_url = self.config.get('defender', {}).get('url', 'http://127.0.0.1:1234')
        lm_studio_url = lm_studio_url.replace('/v1/chat/completions', '')

        self.semantic_detector = HybridDetector(lm_studio_url)

        log_evento("🧠 SemanticDefender inicializado con embedding detection", "INFO")
        log_evento("   Ventaja: Generaliza a paráfrasis nunca vistas", "INFO")

    def evaluate(self, mensaje: str) -> DefenseDecision:
        """
        Evalúa un mensaje usando detección semántica

        Flujo:
        1. Fast path: Pattern matching para casos obvios (microsegundos)
        2. Slow path: Semantic embedding similarity (10-50ms)
        3. LLM Judge como tercer layer (opcional, 1-3s)
        """

        # CAPA 1 + 2: Híbrido (pattern + semantic)
        is_attack, threat_type, confidence, method = self.semantic_detector.detect(mensaje)

        if is_attack:
            log_evento(
                f"🎯 Semantic detection: {threat_type} "
                f"(conf: {confidence:.0%}, method: {method})",
                "INFO"
            )
            return self._process_threat(threat_type, mensaje, from_filter=True)

        # CAPA 3: LLM Judge para casos edge (opcional)
        # Solo si confidence está en zona gris (0.6-0.75)
        if (self.llm_available and
            self.config.get('security', {}).get('use_llm_judge', True) and
            0.6 <= confidence < 0.75):

            log_evento(f"🤔 Confidence en zona gris ({confidence:.0%}), consultando LLM Judge", "DEBUG")

            amenaza_llm = self._llm_judge(mensaje)
            if amenaza_llm:
                log_evento(f"🧠 LLM Judge confirmó: {amenaza_llm}", "INFO")
                return self._process_threat(amenaza_llm, mensaje, from_filter=False)

        # CAPA 4: Sin amenaza detectada
        return DefenseDecision(
            action="PERMITIR",
            risk_score=confidence if confidence < 0.6 else 0.0,
            threat_type=None,
            reasoning=f"Mensaje seguro - similitud semántica baja ({confidence:.0%})",
            vector_state=self.vector.copy()
        )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente LLM para comunicarse con LM Studio (o cualquier API compatible con OpenAI)
"""

import requests
import json
from typing import List, Dict, Optional


class LLMClient:
    """Cliente para interactuar con modelos LLM locales"""

    def __init__(self, base_url: str, model_name: str, temperature: float = 0.7, max_tokens: int = 500):
        """
        Inicializa el cliente LLM

        Args:
            base_url: URL del servidor (ej: http://127.0.0.1:1234/v1/chat/completions)
            model_name: Nombre del modelo
            temperature: Temperatura para generación (0.0 = determinista, 1.0 = creativo)
            max_tokens: Máximo de tokens a generar
        """
        self.base_url = base_url
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        """
        Envía mensajes al LLM y obtiene respuesta

        Args:
            messages: Lista de mensajes en formato [{"role": "user", "content": "..."}]
            temperature: Override temperatura (opcional)

        Returns:
            Respuesta del modelo como string
        """
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando con LLM: {e}")
            return ""
        except (KeyError, IndexError) as e:
            print(f"❌ Error parseando respuesta: {e}")
            return ""

    def simple_prompt(self, prompt: str, temperature: Optional[float] = None) -> str:
        """
        Método simplificado para enviar un prompt directo

        Args:
            prompt: Texto del prompt
            temperature: Override temperatura (opcional)

        Returns:
            Respuesta del modelo
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, temperature)

    def is_available(self) -> bool:
        """
        Verifica si el servidor LLM está disponible

        Returns:
            True si está disponible, False si no
        """
        try:
            # Intentar una solicitud simple
            response = requests.get(
                self.base_url.replace("/chat/completions", "/models"),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Función de utilidad para crear clientes desde config
def create_client_from_config(config: Dict) -> LLMClient:
    """
    Crea un cliente LLM desde un diccionario de configuración

    Args:
        config: Diccionario con keys: url, name, temperature, max_tokens

    Returns:
        Instancia de LLMClient
    """
    return LLMClient(
        base_url=config["url"],
        model_name=config["name"],
        temperature=config.get("temperature", 0.7),
        max_tokens=config.get("max_tokens", 500)
    )

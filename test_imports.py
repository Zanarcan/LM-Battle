#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de imports - ASCII only"""

print("Testing imports...")

try:
    import streamlit as st
    print("[OK] streamlit")
except Exception as e:
    print(f"[FAIL] streamlit: {e}")

try:
    import plotly.graph_objects as go
    print("[OK] plotly.graph_objects")
except Exception as e:
    print(f"[FAIL] plotly: {e}")

try:
    import pandas as pd
    print("[OK] pandas")
except Exception as e:
    print(f"[FAIL] pandas: {e}")

try:
    from src.llm_client import create_client_from_config
    print("[OK] src.llm_client")
except Exception as e:
    print(f"[FAIL] src.llm_client: {e}")

try:
    from src.defender import AxioDefender
    print("[OK] src.defender")
except Exception as e:
    print(f"[FAIL] src.defender: {e}")

try:
    from src.attacker import AdvancedAttacker
    print("[OK] src.attacker")
except Exception as e:
    print(f"[FAIL] src.attacker: {e}")

try:
    from src.utils import load_config
    print("[OK] src.utils")
except Exception as e:
    print(f"[FAIL] src.utils: {e}")

print("\nAll imports tested!")

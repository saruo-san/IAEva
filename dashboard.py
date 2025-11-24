# dashboard.py
import os
import json
from datetime import datetime

import pandas as pd
import streamlit as st

LOG_PATH = os.path.join("storage", "logs", "interactions.jsonl")

st.set_page_config(page_title="Dashboard Observabilidad – IAEva", page_icon="📊", layout="wide")
st.title("📊 Dashboard de Observabilidad – Agente Organizacional")

if not os.path.exists(LOG_PATH):
    st.warning(
        "Aún no hay datos de interacción. Ejecuta primero `app.py` y conversa con el agente para generar logs."
    )
    st.stop()

# --- Carga de datos ---
rows = []
with open(LOG_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(rows)

# Parseo de timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

st.subheader("Resumen general")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("N° de interacciones", len(df))
with col2:
    st.metric("Latencia promedio (ms)", f"{df['latency_ms'].mean():.1f}")
with col3:
    st.metric("Latencia p95 (ms)", f"{df['latency_ms'].quantile(0.95):.1f}")
with col4:
    error_rate = (df["error"].sum() / len(df)) * 100 if len(df) > 0 else 0
    st.metric("% interacciones con error", f"{error_rate:.1f}%")
with col5:
    if "memory_mb" in df.columns and df["memory_mb"].notna().any():
        st.metric("Memoria promedio (MB)", f"{df['memory_mb'].mean():.1f}")
    else:
        st.metric("Memoria promedio (MB)", "N/D")

st.divider()

st.subheader("Evolución de latencia en el tiempo")
df_sorted = df.sort_values("timestamp")
st.line_chart(
    data=df_sorted.set_index("timestamp")["latency_ms"],
    use_container_width=True,
)

st.subheader("Distribución por modo y herramienta")
mode_counts = df["mode"].value_counts().rename_axis("mode").reset_index(name="count")
tool_counts = df["tool"].value_counts().rename_axis("tool").reset_index(name="count")

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(mode_counts.set_index("mode")["count"], use_container_width=True)
    st.caption("N° de interacciones por modo (RAG, WEB, LLM, etc.)")
with col2:
    st.bar_chart(tool_counts.set_index("tool")["count"], use_container_width=True)
    st.caption("N° de interacciones por herramienta usada")

st.subheader("Detalle de últimas interacciones")
st.dataframe(
    df.sort_values("timestamp", ascending=False)[
        ["timestamp", "user_message", "mode", "tool", "latency_ms", "error", "memory_mb"]
    ].head(50),
    use_container_width=True,
)

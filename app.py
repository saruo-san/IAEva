# app.py
import streamlit as st
from agent.core import Agent
from agent.memory import build_vectorstore
from agent.planning import make_plan, decide
from agent.observability import run_with_observability  # <- NUEVO
import os


st.set_page_config(page_title="Agente Organizacional (EP2)", page_icon="🤖", layout="wide")

# Estado
if "chat" not in st.session_state:
    st.session_state.chat = []
if "agent" not in st.session_state:
    st.session_state.agent = Agent()
if "vs_ready" not in st.session_state:
    st.session_state.vs_ready = False

st.title("🤖 Agente Organizacional – Streamlit + Ollama")

with st.sidebar:
    st.header("⚙️ Configuración")
    if st.button("Inicializar Memoria Larga (RAG)"):
        build_vectorstore()
        st.session_state.vs_ready = True
        st.success("VectorStore listo.")

    st.markdown("**Planificación**")
    goal = st.text_input("Objetivo (para planificar):", placeholder="Ej: Preparar reporte semanal de comunicaciones")
    if st.button("Generar plan"):
        if goal.strip():
            steps = make_plan(goal)
            st.session_state.plan = steps
            st.success("Plan generado.")
    if "plan" in st.session_state:
        st.markdown("**Plan actual:**")
        for s in st.session_state.plan:
            st.write(s)

    if st.button("Decidir siguiente paso (demo)"):
        state = "Historial breve:\n" + "\n".join([f"U:{m['u']}\nA:{m['a']}" for m in st.session_state.chat[-3:]])
        decision = decide(state)
        st.info(f"Decisión del agente: {decision}")

    st.divider()
    st.markdown("**Comandos útiles**")
    st.code("guardar: <texto>   # guarda una nota")
    st.code("listar notas       # o 'ver notas'")
    st.code("calc: 2*(3+4)")

# Chat
# Chat
st.subheader("💬 Chat")
user_msg = st.text_input(
    "Escribe tu mensaje:",
    key="user_input",
    placeholder="Ej: ¿Cuál es el procedimiento de onboarding?",
)
if st.button("Enviar"):
    if user_msg.strip():
        chat_history_str = "\n".join(
            [f"Usuario: {m['u']}\nAgente: {m['a']}" for m in st.session_state.chat[-8:]]
        )
        out = run_with_observability(st.session_state.agent, user_msg, chat_history=chat_history_str)
        # Guardamos output + meta (incluye 'metrics')
        st.session_state.chat.append(
            {"u": user_msg, "a": out["output"], "meta": out}
        )
        st.rerun()


# Render del historial
for msg in st.session_state.chat[-10:]:
    with st.chat_message("user"):
        st.markdown(msg["u"])

    with st.chat_message("assistant"):
        st.markdown(msg["a"])

        meta = msg.get("meta", {})

        # Métricas de observabilidad (latencia, memoria, error)
        metrics = meta.get("metrics", {})
        if metrics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱️ Latencia: {metrics.get('latency_ms', 0):.1f} ms")
            with col2:
                mem = metrics.get("memory_mb")
                if mem is not None:
                    st.caption(f"🧠 Memoria proceso: {mem:.1f} MB")
            with col3:
                if metrics.get("error"):
                    st.caption("⚠️ Estado: Error")
                else:
                    st.caption("✅ Estado: OK")

        # Trazas (plan / decisión / herramienta)
        if meta.get("thoughts"):
            with st.expander("🧠 Trazas (plan/decisión/herramienta)"):
                st.write(meta["thoughts"])
                st.write(f"Modo: {meta.get('mode')} | Herramienta: {meta.get('tool')}")

        # Fuentes internas RAG
        if meta.get("sources"):
            st.caption("Fuentes internas (RAG):")
            for s in sorted(set(meta["sources"])):
                st.code(s)


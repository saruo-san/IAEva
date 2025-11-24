# agent/planning.py
from typing import List, Dict
from langchain_community.llms import Ollama

SYSTEM_PROMPT = """Eres un planificador de tareas. Dado un objetivo del usuario, descompón en pasos,
elige herramientas (si aplica) y produce un plan numerado claro. Solo planifica, no ejecutes.
"""

DECISION_PROMPT = """Eres un decisor. Dado un contexto de ejecución y estado, decide:
- si continuar, replanificar, pedir más información o finalizar,
y explica brevemente el por qué."""

def get_llm():
    return Ollama(model="llama3.1")

def make_plan(goal: str) -> List[str]:
    llm = get_llm()
    out = llm.invoke(f"{SYSTEM_PROMPT}\nObjetivo: {goal}\n\nPlan:")
    steps = [s.strip() for s in out.split("\n") if s.strip()]
    # Normalizamos un poco
    numbered = []
    for s in steps:
        if s[0].isdigit():
            numbered.append(s)
        else:
            numbered.append(f"{len(numbered)+1}. {s}")
    return numbered

def decide(next_state_summary: str) -> str:
    llm = get_llm()
    return llm.invoke(f"{DECISION_PROMPT}\n\nContexto:\n{next_state_summary}\n\nDecisión:")

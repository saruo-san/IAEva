# agent/tools.py
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from typing import Any, Dict
import json
from pathlib import Path
import os

NOTES_FILE = Path("storage/notes.json")
NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
if not NOTES_FILE.exists():
    NOTES_FILE.write_text(json.dumps({"notes": []}, ensure_ascii=False, indent=2), encoding="utf-8")

def get_tools():
    # Consulta (web): DuckDuckGo + Wikipedia
    ddg = DuckDuckGoSearchRun()
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(lang="es", top_k_results=3))

    # Escritura (persistencia): notas en JSON
    def write_note_tool(input_text: str) -> str:
        data = json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        data["notes"].append({"text": input_text})
        NOTES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return f"Nota guardada: {input_text[:80]}..."

    def list_notes_tool(_: str = "") -> str:
        data = json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        if not data["notes"]:
            return "No hay notas."
        out = "\n".join([f"- {i+1}. {n['text']}" for i, n in enumerate(data["notes"])])
        return out

    # Razonamiento (cálculo simple) — mini “python” sandbox muy limitado
    def calculator(expr: str) -> str:
        # Seguridad básica: solo números y operadores
        allowed = "0123456789.+-*/() "
        if any(ch not in allowed for ch in expr):
            return "Expresión no permitida."
        try:
            return str(eval(expr))
        except Exception as e:
            return f"Error de cálculo: {e}"

    # Envolvemos en diccionarios tipo LangChain tool definitions simples
    return [
        {
            "name": "duckduckgo_search",
            "description": "Busca información actual en la web con DuckDuckGo.",
            "func": ddg.run,
        },
        {
            "name": "wikipedia",
            "description": "Consulta rápida en Wikipedia (español).",
            "func": wiki.run,
        },
        {
            "name": "write_note",
            "description": "Guarda una nota persistente de texto.",
            "func": write_note_tool,
        },
        {
            "name": "list_notes",
            "description": "Lista notas persistentes guardadas.",
            "func": list_notes_tool,
        },
        {
            "name": "calculator",
            "description": "Calculadora aritmética básica segura.",
            "func": calculator,
        },
    ]

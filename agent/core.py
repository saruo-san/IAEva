# agent/core.py
import os
from typing import Dict, Any
from langchain_community.llms import Ollama
from agent.tools import get_tools
from agent.memory import semantic_retrieve
from textwrap import dedent

SYSTEM = """Eres un agente organizacional. 
Tienes herramientas para: 
- consultar (web/RAG), 
- escribir (notas persistentes), 
- razonar (calculadora), 
y debes mantener coherencia usando contexto previo.

Política de uso:
1) Si la pregunta es sobre la organización o políticas internas, usa primero RAG.
2) Si es información general de la web, usa DuckDuckGo/Wikipedia.
3) Si el usuario pide guardar algo, usa write_note.
4) Si hay cálculos, usa calculator.
Responde en español, con pasos claros y citas de fuentes internas cuando uses RAG (archivo fuente).
"""

def get_llm():
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    return Ollama(model=model, base_url=base)

class Agent:
    def __init__(self):
        self.llm = get_llm()
        self.tools = {t["name"]: t["func"] for t in get_tools()}

    def run(self, user_input: str, chat_history: str = "") -> Dict[str, Any]:
        # Heurística simple: decidir qué herramienta invocar
        thoughts = []
        response = ""

        # 1) Intento RAG si detecto términos internos
        if any(k in user_input.lower() for k in ["política", "procedimiento", "onboarding", "reporte", "comunicación interna"]):
            thoughts.append("RAG: buscando en memoria de largo plazo…")
            hits = semantic_retrieve(user_input, k=4)
            if hits:
                snippets = "\n".join([f"- {h['source']}: {h['content'][:200]}..." for h in hits])
                prompt = dedent(f"""
                {SYSTEM}

                Historial breve:
                {chat_history}

                Contexto interno (RAG):
                {snippets}

                Instrucción:
                Redacta una respuesta clara apoyándote solo en los fragmentos RAG si son relevantes.
                """).strip()
                response = self.llm.invoke(prompt)
                return {"mode": "RAG", "tool": "vectorstore", "thoughts": thoughts, "output": response, "sources": [h["source"] for h in hits]}

        # 2) Web search si parece info general
        if any(k in user_input.lower() for k in ["qué es", "quien es", "fecha", "definición", "define", "últimas noticias", "actualidad"]):
            thoughts.append("Web: probando DuckDuckGo…")
            out = self.tools["duckduckgo_search"](user_input)
            prompt = dedent(f"""
            {SYSTEM}

            Resultados web (DDG):
            {out}

            Tarea: sintetiza respuesta útil y breve.
            """).strip()
            response = self.llm.invoke(prompt)
            return {"mode": "WEB", "tool": "duckduckgo_search", "thoughts": thoughts, "output": response, "sources": []}

        # 3) Persistencia: guardar/listar notas
        if user_input.lower().startswith("guardar:"):
            txt = user_input.split(":", 1)[1].strip()
            thoughts.append("Escritura: guardando nota…")
            res = self.tools["write_note"](txt)
            return {"mode": "WRITE", "tool": "write_note", "thoughts": thoughts, "output": res, "sources": []}

        if user_input.lower() in ["ver notas", "listar notas", "listar mis notas"]:
            thoughts.append("Escritura: listando notas…")
            res = self.tools["list_notes"]("")
            return {"mode": "READ", "tool": "list_notes", "thoughts": thoughts, "output": res, "sources": []}

        # 4) Calculadora
        if user_input.lower().startswith("calc:"):
            expr = user_input.split(":", 1)[1].strip()
            thoughts.append("Razonamiento: calculadora…")
            res = self.tools["calculator"](expr)
            return {"mode": "REASON", "tool": "calculator", "thoughts": thoughts, "output": res, "sources": []}

        # 5) Por defecto: usa LLM “a pelo” con el sistema
        prompt = dedent(f"""
        {SYSTEM}

        Historial:
        {chat_history}

        Usuario: {user_input}
        Agente:
        """).strip()
        response = self.llm.invoke(prompt)
        return {"mode": "LLM", "tool": "none", "thoughts": thoughts, "output": response, "sources": []}

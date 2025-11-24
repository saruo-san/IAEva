# agent/observability.py
import os
import json
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

try:
    import psutil
except ImportError:
    psutil = None  # Por si no está instalado

LOG_DIR = os.path.join("storage", "logs")
LOG_PATH = os.path.join(LOG_DIR, "interactions.jsonl")


def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def _get_memory_mb() -> Optional[float]:
    if psutil is None:
        return None
    proc = psutil.Process(os.getpid())
    return proc.memory_info().rss / (1024 * 1024)


@dataclass
class InteractionLog:
    timestamp: str
    user_message: str
    mode: str
    tool: str
    latency_ms: float
    error: bool
    error_message: Optional[str]
    memory_mb: Optional[float]
    output_chars: int


def log_interaction(entry: InteractionLog) -> None:
    """Guarda una interacción en formato JSONL."""
    _ensure_log_dir()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def run_with_observability(agent, user_input: str, chat_history: str = "") -> Dict[str, Any]:
    """
    Envuelve agent.run para medir latencia, errores y uso de memoria.
    Retorna el mismo dict que agent.run, pero con clave extra 'metrics'.
    """
    start = time.perf_counter()
    error = False
    error_msg = None
    result: Dict[str, Any]

    try:
        result = agent.run(user_input, chat_history=chat_history)
    except Exception as e:
        error = True
        error_msg = str(e)
        # Respuesta segura para el usuario
        result = {
            "mode": "ERROR",
            "tool": "none",
            "thoughts": [],
            "output": "Ocurrió un error interno al ejecutar el agente. Revisa los logs de observabilidad.",
            "sources": [],
        }

    latency_ms = (time.perf_counter() - start) * 1000.0
    memory_mb = _get_memory_mb()
    output_text = result.get("output", "") or ""
    mode = result.get("mode", "unknown")
    tool = result.get("tool", "unknown")

    log_entry = InteractionLog(
        timestamp=datetime.utcnow().isoformat(),
        user_message=user_input,
        mode=mode,
        tool=tool,
        latency_ms=latency_ms,
        error=error,
        error_message=error_msg,
        memory_mb=memory_mb,
        output_chars=len(output_text),
    )
    log_interaction(log_entry)

    # Adjuntamos las métricas en el resultado para mostrarlas en la UI
    result["metrics"] = {
        "latency_ms": latency_ms,
        "memory_mb": memory_mb,
        "error": error,
    }

    return result

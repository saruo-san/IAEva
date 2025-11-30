# IAEva – Agente Organizacional con RAG, LLM, Observabilidad y Dashboard

Este proyecto implementa un **Agente Organizacional Inteligente** capaz de responder preguntas internas de una organización utilizando:

- **RAG (Retrieval Augmented Generation)** para consultar documentos internos.
- **LLM (modelo de lenguaje)** para generar respuestas.
- **Herramientas externas** (búsqueda web).
- **Trazabilidad completa** (planes, decisiones, herramientas utilizadas).
- **Observabilidad** con métricas de latencia, memoria, errores y logs detallados.
- **Dashboard interactivo** construido en Streamlit para analizar el desempeño del agente.

Este README documenta la **arquitectura**, **instalación**, **uso**, **estructura del proyecto** y **nuevas funcionalidades agregadas para la la actualización del proyecto**.

---

# 📂 1. Estructura del proyecto

```
IAEva/
├── agent/
│   ├── core.py             # Lógica principal del agente
│   ├── memory.py           # Construcción del vectorstore (RAG)
│   ├── planning.py         # Planificación, decisiones y trazas
│   ├── tools.py            # Herramientas externas (Web search)
│   ├── observability.py    # NUEVO: Métricas, logs, errores, latencia, memoria
│
├── storage/
│   ├── docs/               # Documentos internos para RAG
│   ├── logs/               # NUEVO: Logs JSONL de interacciones
│       └── interactions.jsonl
│
├── app.py                  # Interfaz principal del agente en Streamlit
├── dashboard.py            # NUEVO: Dashboard de observabilidad
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Este archivo
```

---

# 🧠 2. Descripción general del agente

IAEva es un agente inteligente diseñado para ayudar a empleados dentro de una organización a obtener información clave, documentación interna y asistencia contextual.

El agente opera en **modos automáticos según la consulta**:

| Modo    | Cuándo se activa                           | Fuente                      | Ejemplo                                    |
| ------- | ------------------------------------------ | --------------------------- | ------------------------------------------ |
| **RAG** | Preguntas sobre documentos internos        | Archivos en `storage/docs/` | "Háblame del procedimiento de onboarding"  |
| **LLM** | Preguntas sin contenido interno suficiente | Solo modelo                 | "Dame ideas para mejorar mi productividad" |
| **WEB** | Preguntas externas                         | Búsqueda DuckDuckGo         | "¿Cuál es el precio del dólar hoy?"        |

El agente combina planificación, análisis del mensaje del usuario y selección automática de herramientas.

---

# 📐 3. Arquitectura

El flujo del agente sigue esta secuencia:

```
Usuario → Agente → Planificación → Elección del modo (RAG / WEB / LLM)
        → Ejecución de herramienta (si aplica)
        → Modelo LLM → Respuesta final
        → Trazas + Métricas + Logging
```

### ✔ Planificación (planning.py)

Determina qué modo usar, qué herramientas activar y cómo construir la respuesta.

### ✔ Memoria RAG (memory.py)

Construye un vectorstore usando ChromaDB.

### ✔ Lógica principal (core.py)

Define el comportamiento, los pasos y la integración con las herramientas.

### ✔ Observabilidad (observability.py) – *NUEVO*

Cada interacción registra:

- Latencia (ms)
- Error o éxito
- Mensaje del usuario
- Modo utilizado
- Herramienta utilizada
- Uso de memoria del proceso
- Tamaño de la respuesta generada
- Timestamp

### ✔ Dashboard (dashboard.py) – *NUEVO*

Genera visualizaciones útiles para evaluar desempeño.

---

# 🚀 4. Instalación del proyecto

A continuación se describen los pasos recomendados para levantar el proyecto desde cero en una máquina local.

## 4.1 Clonar el repositorio

Si aún no tienes el proyecto en tu máquina:

```bash
git clone https://github.com/saruo-san/IAEva.git
cd IAEva-main
```

> Si descargaste un ZIP, simplemente descomprímelo y entra a la carpeta `IAEva-main`.

---

## 4.2 Crear entorno virtual

Se recomienda trabajar siempre dentro de un **entorno virtual** para aislar las dependencias del proyecto.

### Windows (PowerShell o CMD)

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Si el entorno está activo, deberías ver algo como:

```bash
(venv) C:\Users\tu_usuario> _
```

---

## 4.3 Actualizar `pip` (opcional pero recomendado)

```bash
python -m pip install --upgrade pip
```

---

## 4.4 Instalar dependencias

Con el entorno virtual activo, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### Posibles problemas en Windows

- **Error al compilar ****`chroma-hnswlib`**** / ****`chromadb`**\
  Asegúrate de tener instalado **Microsoft C++ Build Tools** (MSVC v14.x o superior) con la carga de trabajo *"Desarrollo de escritorio con C++"*.

- **Error ****`ImportError: Could not import ddgs python package`**\
  Instala explícitamente las dependencias del buscador web:

  ```bash
  pip install -U ddgs duckduckgo-search
  ```

Con esto el proyecto queda listo para ejecutar.

---

# 🔑 5. Variables de entorno

Este proyecto \*\*utiliza modelos locales ejecutados mediante **Ollama**, por lo que no requiere API keys externas como OpenAI.

Para que el agente funcione correctamente, es necesario tener **Ollama instalado** y un modelo cargado (por ejemplo: `llama3`, `mistral`, etc.).

El agente se comunica con Ollama de manera local usando su servidor interno (`http://localhost:11434`).

> ✨ **Importante:** El agente utiliza documentos internos (RAG) y modelos locales definidos en el código. No depende de servicios externos.

---

# ▶ 6. Ejecutar el agente

```
streamlit run app.py
```

Esto abrirá la interfaz de chat con:

- Mensaje del usuario
- Respuesta del agente
- Expansores con **trazas internas** (plan, modo, herramienta)
- Métricas debajo de cada respuesta (latencia, memoria, estado)

Cada interacción se guarda en:

```
storage/logs/interactions.jsonl
```

---

# 📊 7. Dashboard de observabilidad

Ejecutar:

```
streamlit run dashboard.py
```

El dashboard muestra:

### ✔ Resumen general

- N° de interacciones
- Latencia promedio
- Latencia p95
- % de errores
- Memoria promedio del proceso

### ✔ Gráfico: Evolución de latencia

Visualiza cómo cambia la latencia a lo largo del tiempo.

### ✔ Gráfico: Distribución de modo

Permite ver qué tan frecuentemente se usa RAG, WEB o LLM.

### ✔ Gráfico: Distribución de herramientas

Muestra cuántas veces se usó `vectorstore`, `web`, o ninguna herramienta.

### ✔ Tabla de últimas interacciones

Incluye timestamp, mensaje, modo, herramienta, latencia y error.

---

# 📁 8. Logging (Formato JSONL)

Las interacciones se guardan en líneas independientes con este formato:

```json
{
  "timestamp": "2025-11-24T18:30:20.023367",
  "user_message": "¿A qué hora se entregan los reportes semanales?",
  "mode": "RAG",
  "tool": "vectorstore",
  "latency_ms": 7757.6682,
  "error": false,
  "error_message": null,
  "memory_mb": 195.3789,
  "output_chars": 842
}
```

Estos logs permiten:

- Evaluar desempeño
- Identificar cuellos de botella
- Auditar interacciones
- Justificar decisiones técnicas en el informe la actualización del proyecto

---

# 🛠 9. Herramientas del agente

### 📌 RAG – Recuperación de Información Interna

Usa ChromaDB para buscar fragmentos relevantes en:

```
storage/docs/*.md
```

### 📌 Web Search

Usa DuckDuckGo vía `duckduckgo-search` o `ddgs`.

### 📌 Generación LLM

Base para todas las respuestas finales del agente.

---

# 🔍 10. Observabilidad – Funcionalidades agregadas

Estas funcionalidades fueron implementadas para cumplir la la actualización del proyecto:

### ✔ Logging detallado (JSONL)

### ✔ Métricas por interacción

- Latencia
- Memoria del proceso
- Tamaño de salida
- Errores

### ✔ UI del agente muestra trazabilidad

- Modo usado
- Herramienta usada
- Plan
- Decisiones internas

### ✔ Dashboard visual con Streamlit

Cumple requisitos IE5, IE6, IE7, IE8.

---

# 🧪 11. Testing manual recomendado

Ejemplos de consultas:

- "Háblame del archivo procedimientos.md"
- "¿Qué documentos existen para onboarding?"
- "Dame recomendaciones para mejorar la comunicación interna"
- "¿Qué hora es en Nueva York?" (prueba de Web Search)

---

# 📌 12. Problemas comunes y soluciones

| Problema                   | Causa                    | Solución                                |
| -------------------------- | ------------------------ | --------------------------------------- |
| Error al instalar chromadb | Falta de C++ Build Tools | Instalar MSVC v142 o superior           |
| Error DDGS                 | Faltan dependencias      | `pip install -U ddgs duckduckgo-search` |
| API no responde            | Falta OPENAI\_API\_KEY   | Crear `.env`                            |

---

# 🖼️ 13. Evidencias del proyecto

En esta sección se pueden incluir capturas relacionadas con el funcionamiento del agente y las funcionalidades agregadas.

### 🔹 Evidencia 1: Interacciones del agente

<img width="1881" height="925" alt="1" src="https://github.com/user-attachments/assets/3407a4f5-2dc4-4b01-a3a6-5358a7a30ab3" />

### 🔹 Evidencia 2: Logs de observabilidad

<img width="1467" height="214" alt="4" src="https://github.com/user-attachments/assets/ae165648-b4d1-45ce-b351-872c518b9137" />

### 🔹 Evidencia 3: Dashboard de métricas

<img width="1820" height="734" alt="2" src="https://github.com/user-attachments/assets/45e26413-99a4-474f-820c-1acac8271913" />

<img width="1758" height="765" alt="3" src="https://github.com/user-attachments/assets/4ae211d8-680b-433a-96f1-369d121b8ed7" />

---

# 🧾 14. Créditos

Proyecto base: [https://github.com/saruo-san/IAEva](https://github.com/saruo-san/IAEva)\
Modificaciones y extensiones realizadas por Javier Muñoz y Matias Cerda como parte de la evolución del proyecto.

---

# 📄 14. Licencia

Este proyecto se distribuye con fines de mejora y mantenimiento continuo y puede ser extendido libremente.

---

# 📚 15. Entregables del EFT

- `notebooks/AgenteDemo.ipynb+`: notebook demostrativo (RAG, agente, métricas, trazas).
- Evidencias: usar `docs/evidence/` para capturas y gráficos.

## Requisitos adicionales (EFT)
- Python 3.10+
- Paquetes del `requirements.txt`

## Pasos rápidos en Windows PowerShell
```powershell
pip install -r requirements.txt
python app.py
python dashboard.py
```


# 🤖 Agente Organizacional – Streamlit + Ollama  
**Proyecto Evaluación 2 – Inteligencia Artificial**

![Streamlit App Screenshot](https://raw.githubusercontent.com/saruo-san/IAEva/main/docs/captura_evidencia.png)

---

## 📋 Descripción General

Este proyecto implementa un **Agente Organizacional Inteligente**, desarrollado con **Python, Streamlit y Ollama**, que combina:

- 🔍 **Consulta de información** (web y fuentes internas)
- 🧠 **Memoria de largo y corto plazo** (RAG + contexto de chat)
- 🛠️ **Herramientas de escritura, razonamiento y cálculo**
- 🗂️ **Recuperación semántica (RAG) con embeddings**
- 🧩 **Planificación y toma de decisiones**
- 💬 **Interfaz interactiva con Streamlit**

El agente es capaz de responder preguntas sobre políticas internas, generar planes de acción, realizar cálculos simples, guardar notas y mantener coherencia en las conversaciones.

---

## 🧱 Estructura del Proyecto

- agente-streamlit-ep2/
- ├─ agent/
- │ ├─ core.py # Núcleo del agente (orquestación de herramientas y RAG)
- │ ├─ memory.py # Memoria de corto y largo plazo
- │ ├─ tools.py # Herramientas de consulta, escritura y cálculo
- │ └─ planning.py # Planificación y toma de decisiones
- │
- ├─ data/knowledge/ # Base de conocimiento interna (archivos .md)
- │ ├─ politicas.md
- │ └─ procedimientos.md
- │
- ├─ storage/chroma/ # VectorStore persistente (se genera automáticamente)
- │
- ├─ docs/ # Evidencias o diagramas
- │ └─ arquitectura.mmd # Diagrama Mermaid
- │
- ├─ app.py # Interfaz Streamlit
- ├─ requirements.txt # Dependencias del proyecto
- └─ README.md # Este archivo

---

## ⚙️ Instalación y Configuración

### 1️⃣ Requisitos previos

- Python **3.10 o 3.11**
- [Ollama](https://ollama.com) instalado y corriendo localmente
- Modelos descargados:
  ```bash
  ollama pull llama3.1
  ollama pull nomic-embed-text

- 2️⃣ Clonar el repositorio
git clone https://github.com/saruo-san/IAEva.git
cd IAEva

- 3️⃣ Crear entorno virtual
python -m venv .venv
.\.venv\Scripts\activate

- 4️⃣ Instalar dependencias
pip install -r requirements.txt

- 5️⃣ Ejecutar Ollama (en otra consola)
ollama serve

- 6️⃣ Iniciar la aplicación
streamlit run app.py


Luego abre el enlace local (por defecto: http://localhost:8501
).

💡 Cómo usar el agente
🧠 Inicializar memoria larga (RAG)

En la barra lateral:

Presiona "Inicializar Memoria Larga (RAG)"
Esto cargará los archivos .md desde data/knowledge.

💬 Chat interactivo

Prueba con:

¿A qué hora se entregan los reportes semanales?
¿Cuál es el procedimiento de onboarding?
guardar: Llamar al proveedor el lunes
listar notas
calc: (12/3)+8

## 🗓️ Planificación y decisiones

En la barra lateral:

Escribe un objetivo en el campo “Objetivo (para planificar)”

Pulsa Generar plan

Luego Decidir siguiente paso (demo)

##📚 Funcionalidades principales
Categoría	Descripción	Archivo responsable

- 🔍 Consulta Web	Usa DuckDuckGo y Wikipedia	agent/tools.py
- 🧠 Memoria Semántica	RAG con Ollama Embeddings + Chroma	agent/memory.py
- 📝 Escritura Persistente	Guarda y lista notas locales	agent/tools.py
- 🧮 Razonamiento	Calculadora simple segura	agent/tools.py
- 🗓️ Planificación	Genera planes paso a paso	agent/planning.py
- ⚖️ Decisión	Evalúa próximos pasos según contexto	agent/planning.py
- 💬 UI	Interfaz con Streamlit	app.py
- 🧩 Ejemplos de prueba

Tipo de prueba	Prompt sugerido	Resultado esperado
- RAG (memoria interna)	“¿Cuál es el procedimiento de onboarding?”	Cita data/knowledge/procedimientos.md
- Escritura	“guardar: Reunión con comunicaciones el jueves”	Nota guardada en storage/notes.json
- Listar notas	“listar notas”	Muestra todas las notas
- Razonamiento	“calc: 2*(5+3)”	Devuelve 16
- Web	“¿Qué es inteligencia artificial?”	Resumen desde la web
- Planificación	Objetivo: “Preparar reporte semanal”	Genera pasos numerados
- Decisión	Botón “Decidir siguiente paso”	Devuelve recomendación

## 🧠 Diagrama de Arquitectura
flowchart LR
    U[Usuario] -->|Mensaje| S[Streamlit UI]
    S --> A[Agent Core]
    A -->|Heurística| T[Tools]
    A -->|RAG| V[VectorStore Chroma]
    V --> E[Ollama Embeddings]
    A -->|LLM| L[Ollama llama3.1]
    T -->|consulta| W[DuckDuckGo/Wikipedia]
    T -->|escritura| N[notes.json]
    T -->|razonamiento| C[Calculator]
    subgraph Planificación
      P1[make_plan] --> P2[decide]
    end
    S -->|Planificación| P1
    P2 --> A

<img width="1163" height="373" alt="Captura de pantalla 2025-10-27 172732" src="https://github.com/user-attachments/assets/dd0818ca-637a-47f6-8d39-af39b8774752" />


## 🖼️ Evidencias

- Chat RAG respondiendo “¿A qué hora se entregan los reportes semanales?”
- Chat con “guardar:” y luego “listar notas”
- Plan generado en el panel lateral
- Botón de decisión funcionando

<img width="1875" height="817" alt="Captura de pantalla 2025-10-27 172040" src="https://github.com/user-attachments/assets/42cd4789-c573-49d0-9bcf-82053c86952d" />



## 🧾 Créditos

Desarrollado por:
👨‍💻 Javier Muñoz y Matias Cerda
📘 Asignatura: Inteligencia Artificial – Evaluación 2 (IAEva)
🏫 Instituto Profesional DuocUC/ Año 2025

🧩 Licencia

Este proyecto se distribuye con fines educativos bajo la licencia MIT.
Puedes usarlo, modificarlo y compartirlo libremente citando la fuente.


Documentación de Herramientas de IA Utilizadas en el Proyecto IAEva

Este documento resume las tecnologías, librerías y enfoques de inteligencia artificial empleadas dentro del proyecto IAEva, detallando su función dentro del agente, el procesamiento de información y los servicios de apoyo utilizados.

🧠 1. Lenguaje y Frameworks de Agentes
### LangChain

El proyecto utiliza LangChain como la base para la construcción del agente inteligente. Esta librería permite estructurar las interacciones del modelo, manejar herramientas externas y crear flujos más complejos que combinan memoria, planificación y recuperación de información.

Componentes usados:

langchain_core
langchain
langchain_community
Funciones principales dentro del proyecto:
Creación de agentes personalizados.
Manejo de prompts dinámicos.
Integración con VectorStores.
Uso de herramientas de búsqueda y recuperación.

🧩 2. Modelos de Lenguaje
### Ollama

El sistema se apoya en Ollama para ejecutar modelos de lenguaje localmente.
Se utiliza en dos áreas principales:

Generación de lenguaje: El agente usa modelos LLM para resolver consultas, crear explicaciones y planificar.

Embeddings: Se generan vectores semánticos mediante OllamaEmbeddings.

Esto permite:

Mayor privacidad al no depender de servicios externos.

Respuestas más rápidas en tareas locales.

Flexibilidad para usar distintos modelos.

🗃️ 3. Vector Store y Recuperación Semántica
### ChromaDB

La herramienta Chroma funciona como base vectorial para almacenar y recuperar conocimiento del proyecto.

Implementaciones del proyecto:

Construcción de un vectorstore para documentos en data/knowledge.

Uso de embeddings para búsquedas semánticas.

Integración mediante funciones de “semantic retrieve”.

Esto permite que el agente:

Acceda a información previa del dominio.

Realice análisis contextualizados.

Entienda contenido largo dividido por fragmentos.

### Text Splitters

Se emplea RecursiveCharacterTextSplitter para dividir documentos extensos en fragmentos manejables antes de cargarlos al vector store.

🔎 4. Herramientas de Búsqueda y Fuentes Externas
### DuckDuckGoSearchRun

Permite realizar búsquedas en la web sin depender de APIs cerradas.
El agente usa esta herramienta cuando requiere:

Información actualizada.

Verificación de datos externos.

Ampliar contexto en tiempo real.

### WikipediaAPIWrapper

Facilita obtener datos estructurados desde Wikipedia.
Usos típicos:

Consultas de definiciones.

Búsqueda de eventos, lugares o biografías.

Obtención de contexto general.

🗂️ 5. Observabilidad y Monitoreo
### Módulos propios del proyecto

Dentro de la carpeta agent/, se incorporan herramientas internas para mejorar el comportamiento del agente:

planning.py
Mecanismo de planificación que permite que el agente estructure sus pasos.

memory.py
Maneja una memoria persistente en formato JSON, almacenando notas y contexto relevante.

observability.py
Funciones para registrar actividades, medir tiempos y facilitar el seguimiento del agente.

tools.py
Centraliza las herramientas externas utilizadas por LangChain.

📂 6. Procesamiento y Soporte General

Aunque no son herramientas de IA, algunas librerías complementan el funcionamiento del sistema:

pandas (manejo de datos)

psutil (información del sistema)

streamlit (interfaz gráfica del dashboard)

Pathlib / JSON / OS (gestión de archivos del agente)

📑 7. Conjuntos de Conocimiento del Proyecto

En data/knowledge se almacena el conocimiento estructurado que se indexa mediante embeddings:

politicas.md

procedimientos.md

Estos documentos alimentan el vector store y permiten que el agente responda con conocimiento contextual propio de la organización.

✔️ Resumen General
Componente	Rol en el Proyecto
LangChain	Marco central del agente
Ollama	LLM + embeddings locales
ChromaDB	Vector store para memoria semántica
DuckDuckGoSearchRun	Búsqueda web
WikipediaAPIWrapper	Datos externos estructurados
Text Splitters	Procesamiento documental
Módulos de agente propios	Planificación, memoria, observabilidad
# agent/memory.py
import os
from typing import List, Dict
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path

# Memoria de corto plazo: buffer en sesión (lo lleva Streamlit/agent)
# Memoria de largo plazo: RAG con Chroma + OllamaEmbeddings

def build_vectorstore(knowledge_dir: str = "data/knowledge", persist_dir: str = "storage/chroma"):
    embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model, base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

    docs: List[Document] = []
    base = Path(knowledge_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    for fp in base.glob("**/*.md"):
        text = fp.read_text(encoding="utf-8")
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"source": str(fp)}))

    vs = Chroma.from_documents(docs, embedding=embeddings, persist_directory=persist_dir)
    vs.persist()
    return vs

def get_vectorstore(persist_dir: str = "storage/chroma"):
    embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model, base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    return Chroma(embedding_function=embeddings, persist_directory=persist_dir)

def semantic_retrieve(query: str, k: int = 4) -> List[Dict]:
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=k)
    return [{"content": d.page_content, "source": d.metadata.get("source")} for d in docs]

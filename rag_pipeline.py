# rag_pipeline.py
# AI Learning & Study Assistant -- RAG pipeline using local Ollama models
# No API key needed. Everything runs locally.

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_classic.chains import RetrievalQA


# ---------- Step 1: Load document ----------
def load_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from {file_path}")
    return documents


# ---------- Step 2: Split into chunks ----------
def split_into_chunks(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


# ---------- Step 3: Create embeddings + store in ChromaDB ----------
def create_vector_store(chunks, persist_directory="./chroma_db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("Vector store created and saved to", persist_directory)
    return vector_store


# ---------- Step 4: Load an existing vector store (skip re-embedding) ----------
def load_vector_store(persist_directory="./chroma_db"):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vector_store


# ---------- Step 5: Ask a question using RAG (retrieval + local LLM) ----------
def ask_question(vector_store, question, top_k=3):
    llm = OllamaLLM(model="llama3.2")

    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    result = qa_chain.invoke({"query": question})

    print("\n--- Answer ---")
    print(result["result"])

    print("\n--- Sources used ---")
    for i, doc in enumerate(result["source_documents"], 1):
        page = doc.metadata.get("page", "?")
        print(f"[{i}] Page {page}: {doc.page_content[:150]}...")

    return result


# ---------- Main ----------
if __name__ == "__main__":
    file_path = "sample_notes.pdf"   # your PDF path here
    persist_directory = "./chroma_db"

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("Existing vector store found. Loading it (skipping re-embedding)...")
        vector_store = load_vector_store(persist_directory)
    elif os.path.exists(file_path):
        docs = load_document(file_path)
        chunks = split_into_chunks(docs)
        vector_store = create_vector_store(chunks, persist_directory)
    else:
        print(f"File not found: {file_path}. Add a sample PDF first.")
        exit()

    # Test question
    question = "What are the subjects in 3rd semester?"
    ask_question(vector_store, question)
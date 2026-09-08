# agent.py
# AI Learning & Study Assistant -- Agent core
# Combines: RAG (course material retrieval) + Memory (student history) + LLM

import os
from langchain_ollama import OllamaLLM
from rag_pipeline import load_vector_store, load_document, split_into_chunks, create_vector_store
import memory_store as memory


LLM_MODEL = "qwen2.5:7b"


def build_prompt(question, retrieved_chunks, memory_context):
    """Combine retrieved course content + student memory into one prompt."""
    context_text = "\n\n".join(doc.page_content for doc in retrieved_chunks)

    prompt = f"""You are a study assistant for a college student. Answer ONLY using the course material given below.

Rules:
- If the course material does not contain the answer, reply exactly: "This isn't covered in your course material. Would you like me to explain it in general terms instead?"
- Do not use outside knowledge unless the student explicitly asks for a general explanation after that.
- Keep answers clear, simple, and student-friendly.

Course material:
{context_text}

{memory_context}

Student's question: {question}

Answer:"""
    return prompt


def ask_agent(student_id, question, vector_store, top_k=3, relevance_threshold=0.6):
    # 1. Retrieve relevant chunks WITH similarity scores (RAG)
    # Chroma's default score is a distance -- LOWER means MORE similar.
    results_with_scores = vector_store.similarity_search_with_score(question, k=top_k)

    if not results_with_scores:
        answer = "This isn't covered in your course material. Would you like me to explain it in general terms instead?"
        memory.save_conversation(student_id, question, answer)
        return answer, []

    best_score = results_with_scores[0][1]
    retrieved_chunks = [doc for doc, score in results_with_scores]

    print(f"[debug] best_score = {best_score:.4f}  (all scores: {[round(s,4) for _, s in results_with_scores]})")

    # If even the closest chunk is too far (distance too high), treat as out-of-scope.
    if best_score > relevance_threshold:
        answer = "This isn't covered in your course material. Would you like me to explain it in general terms instead?"
        memory.save_conversation(student_id, question, answer)
        return answer, retrieved_chunks

    # 2. Pull memory context (past conversation + weak topics)
    memory_context = memory.build_memory_context(student_id)

    # 3. Build the full prompt
    prompt = build_prompt(question, retrieved_chunks, memory_context)

    # 4. Call the local LLM
    llm = OllamaLLM(model=LLM_MODEL)
    answer = llm.invoke(prompt)

    # 5. Save this exchange to memory
    memory.save_conversation(student_id, question, answer)

    return answer, retrieved_chunks


if __name__ == "__main__":
    memory.init_db()

    student_id = "student1"
    file_path = "sample_notes.pdf"
    persist_directory = "./chroma_db"

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        vector_store = load_vector_store(persist_directory)
    elif os.path.exists(file_path):
        docs = load_document(file_path)
        chunks = split_into_chunks(docs)
        vector_store = create_vector_store(chunks, persist_directory)
    else:
        print(f"File not found: {file_path}")
        exit()

    print("Study Assistant ready. Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.strip().lower() == "exit":
            break

        answer, sources = ask_agent(student_id, question, vector_store)

        print("\nAssistant:", answer)
        print("\n(Sources: pages", [doc.metadata.get("page", "?") for doc in sources], ")\n")
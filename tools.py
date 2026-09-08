# tools.py
# AI Learning & Study Assistant -- Tools: Quiz generator + Study plan generator

import json
import re
from langchain_ollama import OllamaLLM

LLM_MODEL = "qwen2.5:7b"


def _clean_json_response(text):
    """LLMs sometimes wrap JSON in ```json fences or add extra text. Strip that."""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"```\s*$", "", text)
    return text.strip()


# ---------- Tool 1: Quiz generator ----------
def generate_quiz(topic, vector_store, num_questions=5, top_k=6):
    """
    Retrieve course content about `topic` and ask the LLM to generate
    a multiple-choice quiz in structured JSON.
    """
    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    retrieved_chunks = retriever.invoke(topic)
    context_text = "\n\n".join(doc.page_content for doc in retrieved_chunks)

    prompt = f"""You are creating a quiz for a college student based ONLY on the course material below.

Course material:
{context_text}

Create {num_questions} multiple-choice questions about "{topic}" using ONLY the information above.

Respond with ONLY valid JSON in this exact format, no extra text:
[
  {{
    "question": "...",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correct_answer": "A",
    "explanation": "..."
  }}
]
"""

    llm = OllamaLLM(model=LLM_MODEL)
    raw_response = llm.invoke(prompt)
    cleaned = _clean_json_response(raw_response)

    try:
        quiz = json.loads(cleaned)
        return quiz
    except json.JSONDecodeError:
        print("[warning] Could not parse quiz as JSON. Raw LLM output:\n", raw_response)
        return None


def run_quiz(quiz, student_id, topic, memory_module):
    """Interactively ask the quiz questions in the terminal and score it."""
    if not quiz:
        print("No quiz available.")
        return

    score = 0
    total = len(quiz)

    for i, q in enumerate(quiz, 1):
        print(f"\nQ{i}. {q['question']}")
        for key, option in q["options"].items():
            print(f"   {key}. {option}")

        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == q["correct_answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. Correct answer: {q['correct_answer']} - {q.get('explanation', '')}")

    print(f"\nFinal score: {score}/{total}")
    memory_module.save_quiz_score(student_id, topic, score, total)
    memory_module.mark_topic(student_id, topic, status="completed" if score / total >= 0.7 else "in_progress")
    return score, total


# ---------- Tool 2: Study plan generator ----------
def generate_study_plan(subject, num_days, vector_store=None, top_k=8):
    """
    Generate a day-by-day study plan for a subject.
    If a vector_store is given, pull real topic names from the course material.
    """
    context_text = ""
    if vector_store is not None:
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        retrieved_chunks = retriever.invoke(subject)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_chunks)

    prompt = f"""Create a {num_days}-day study plan for the subject "{subject}" for a college student.

{"Use these course topics as reference:" if context_text else ""}
{context_text}

Respond with ONLY valid JSON in this exact format, no extra text:
{{
  "subject": "{subject}",
  "days": [
    {{"day": 1, "topics": ["...", "..."], "goal": "..."}},
    {{"day": 2, "topics": ["...", "..."], "goal": "..."}}
  ]
}}

Spread the topics evenly across {num_days} days, from basic concepts to more advanced ones.
"""

    llm = OllamaLLM(model=LLM_MODEL)
    raw_response = llm.invoke(prompt)
    cleaned = _clean_json_response(raw_response)

    try:
        plan = json.loads(cleaned)
        return plan
    except json.JSONDecodeError:
        print("[warning] Could not parse study plan as JSON. Raw LLM output:\n", raw_response)
        return None


def print_study_plan(plan):
    if not plan:
        print("No study plan available.")
        return
    print(f"\nStudy Plan: {plan['subject']}")
    for day in plan["days"]:
        print(f"\nDay {day['day']}: {day['goal']}")
        for topic in day["topics"]:
            print(f"  - {topic}")


if __name__ == "__main__":
    # Quick manual test (requires an existing chroma_db from rag_pipeline.py)
    from rag_pipeline import load_vector_store
    import memory_store as memory
    import os

    memory.init_db()

    if not os.path.exists("./chroma_db"):
        print("No vector store found. Run rag_pipeline.py first.")
        exit()

    vector_store = load_vector_store("./chroma_db")

    print("=== Testing quiz generator ===")
    quiz = generate_quiz("Democratic Values", vector_store, num_questions=3)
    if quiz:
        run_quiz(quiz, "student1", "Democratic Values", memory)

    print("\n=== Testing study plan generator ===")
    plan = generate_study_plan("Human Values and Ethics", num_days=5, vector_store=vector_store)
    print_study_plan(plan)
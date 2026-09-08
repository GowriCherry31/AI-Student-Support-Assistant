# memory_store.py
# AI Learning & Study Assistant -- Memory layer (SQLite)
# Tracks: conversation history, topics covered, quiz scores

import sqlite3
from datetime import datetime


DB_PATH = "student_memory.db"


def init_db(db_path=DB_PATH):
    """Create tables if they don't exist yet."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            question TEXT,
            answer TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics_covered (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            topic TEXT,
            status TEXT,      -- 'in_progress' or 'completed'
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            topic TEXT,
            score INTEGER,
            total INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized:", db_path)


# ---------- Conversation history ----------
def save_conversation(student_id, question, answer, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversation_history (student_id, question, answer, timestamp) VALUES (?, ?, ?, ?)",
        (student_id, question, answer, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_recent_conversations(student_id, limit=5, db_path=DB_PATH):
    """Fetch the last N Q&A pairs for this student, oldest first."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT question, answer FROM conversation_history
           WHERE student_id = ?
           ORDER BY id DESC LIMIT ?""",
        (student_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))  # oldest first, for natural reading order


# ---------- Topics ----------
def mark_topic(student_id, topic, status="in_progress", db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO topics_covered (student_id, topic, status, timestamp) VALUES (?, ?, ?, ?)",
        (student_id, topic, status, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_topics(student_id, status=None, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if status:
        cursor.execute(
            "SELECT topic, status FROM topics_covered WHERE student_id = ? AND status = ?",
            (student_id, status)
        )
    else:
        cursor.execute(
            "SELECT topic, status FROM topics_covered WHERE student_id = ?",
            (student_id,)
        )
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- Quiz scores ----------
def save_quiz_score(student_id, topic, score, total, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_scores (student_id, topic, score, total, timestamp) VALUES (?, ?, ?, ?, ?)",
        (student_id, topic, score, total, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_weak_topics(student_id, threshold=0.5, db_path=DB_PATH):
    """Return topics where the student scored below the threshold (e.g. 50%)."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT topic, score, total FROM quiz_scores WHERE student_id = ?",
        (student_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    weak = []
    for topic, score, total in rows:
        if total > 0 and (score / total) < threshold:
            weak.append((topic, score, total))
    return weak


# ---------- Build a memory summary for the LLM prompt ----------
def build_memory_context(student_id, db_path=DB_PATH):
    """
    Produces a short text block summarizing what we remember about
    this student, to inject into the LLM prompt.
    """
    recent = get_recent_conversations(student_id, limit=3, db_path=db_path)
    weak_topics = get_weak_topics(student_id, db_path=db_path)

    context_parts = []

    if recent:
        context_parts.append("Recent conversation:")
        for q, a in recent:
            context_parts.append(f"Q: {q}\nA: {a}")

    if weak_topics:
        topics_str = ", ".join(t[0] for t in weak_topics)
        context_parts.append(f"\nStudent is weak in: {topics_str}. Explain simply if these come up.")

    return "\n".join(context_parts) if context_parts else ""


if __name__ == "__main__":
    # quick manual test
    init_db()
    save_conversation("student1", "What is RAG?", "RAG stands for Retrieval-Augmented Generation.")
    mark_topic("student1", "RAG basics", status="completed")
    save_quiz_score("student1", "RAG basics", 3, 10)

    print("\n--- Recent conversations ---")
    print(get_recent_conversations("student1"))

    print("\n--- Weak topics ---")
    print(get_weak_topics("student1"))

    print("\n--- Memory context for prompt ---")
    print(build_memory_context("student1"))

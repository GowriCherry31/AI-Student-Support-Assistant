# app.py
# AI Learning & Study Assistant -- Streamlit frontend (multi-subject)
# Run with: streamlit run app.py

import os
import streamlit as st

from rag_pipeline import load_document, split_into_chunks, create_vector_store, load_vector_store
import memory_store as memory
from agent import ask_agent
from tools import generate_quiz, generate_study_plan

STUDENT_ID = "student1"  # single-student demo; could be extended to a login system
MATERIALS_DIR = "./materials"
CHROMA_ROOT = "./chroma_db"

os.makedirs(MATERIALS_DIR, exist_ok=True)
os.makedirs(CHROMA_ROOT, exist_ok=True)

st.set_page_config(page_title="AI Learning & Study Assistant", page_icon="📚", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    h1 {
        color: #1E293B;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #2563EB;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        padding: 0 18px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: white !important;
    }
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 10px 14px;
        margin-bottom: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        background-color: #F1F5F9;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius: 14px;
    }
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        background-color: #F8FAFC;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

memory.init_db()


# ---------- Helpers for multi-subject storage ----------
def list_subjects():
    """Each subject = one PDF in MATERIALS_DIR, named <subject>.pdf"""
    if not os.path.exists(MATERIALS_DIR):
        return []
    return sorted(f[:-4] for f in os.listdir(MATERIALS_DIR) if f.lower().endswith(".pdf"))


def subject_persist_dir(subject):
    return os.path.join(CHROMA_ROOT, subject)


@st.cache_resource
def get_vector_store_for(subject):
    persist_dir = subject_persist_dir(subject)
    pdf_path = os.path.join(MATERIALS_DIR, f"{subject}.pdf")

    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return load_vector_store(persist_dir)
    elif os.path.exists(pdf_path):
        docs = load_document(pdf_path)
        chunks = split_into_chunks(docs)
        return create_vector_store(chunks, persist_dir)
    return None


def add_subject(subject_name, uploaded_file):
    """Save the uploaded PDF and build its vector store."""
    safe_name = "".join(c for c in subject_name if c.isalnum() or c in (" ", "-", "_")).strip()
    if not safe_name:
        return None

    pdf_path = os.path.join(MATERIALS_DIR, f"{safe_name}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    persist_dir = subject_persist_dir(safe_name)
    docs = load_document(pdf_path)
    chunks = split_into_chunks(docs)
    create_vector_store(chunks, persist_dir)

    get_vector_store_for.clear()  # bust cache so the new subject loads fresh
    return safe_name


# ---------- Sidebar: subject picker + uploader ----------
st.sidebar.header("📂 Subjects")

subjects = list_subjects()

if subjects:
    selected_subject = st.sidebar.selectbox("Active subject", subjects)
else:
    selected_subject = None
    st.sidebar.info("No subjects yet. Add your first course PDF below.")

st.sidebar.divider()
st.sidebar.subheader("➕ Add a new subject")
new_subject_name = st.sidebar.text_input("Subject name", placeholder="e.g. Data Structures")
new_subject_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

if st.sidebar.button("Add Subject", disabled=not (new_subject_name and new_subject_file)):
    with st.spinner(f"Processing '{new_subject_name}'..."):
        added = add_subject(new_subject_name, new_subject_file)
    if added:
        st.sidebar.success(f"Added '{added}'!")
        st.rerun()
    else:
        st.sidebar.error("Please enter a valid subject name.")


# ---------- Main area ----------
st.title("📚 AI Learning & Study Assistant")
st.caption("Ask questions, test yourself, and plan your study time — powered by your own course material.")

if not selected_subject:
    st.warning("👈 Add a subject PDF from the sidebar to get started.")
    st.stop()

st.markdown(f"**Studying:** `{selected_subject}`")
vector_store = get_vector_store_for(selected_subject)

if vector_store is None:
    st.error("Could not load this subject's material. Try re-uploading it.")
    st.stop()

tab_chat, tab_quiz, tab_plan, tab_progress = st.tabs(
    ["💬 Ask a Question", "📝 Quiz Me", "🗓️ Study Plan", "📊 My Progress"]
)


# ---------- Tab 1: Chat ----------
with tab_chat:
    header_col, clear_col = st.columns([5, 1])
    with header_col:
        st.subheader(f"Ask anything from {selected_subject}")
    with clear_col:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state[f"chat_history_{selected_subject}"] = []
            st.rerun()

    history_key = f"chat_history_{selected_subject}"
    if history_key not in st.session_state:
        st.session_state[history_key] = []

    if not st.session_state[history_key]:
        st.info("💡 Ask a question about your uploaded course material to get started.")

    for role, msg in st.session_state[history_key]:
        avatar = "🧑‍🎓" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.write(msg)

    question = st.chat_input("Type your question...")
    if question:
        st.session_state[history_key].append(("user", question))
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.write(question)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                answer, sources = ask_agent(STUDENT_ID, question, vector_store)
            st.write(answer)
            if sources:
                pages = sorted(set(doc.metadata.get("page", "?") for doc in sources))
                st.caption(f"📄 Sources: pages {pages}")

        st.session_state[history_key].append(("assistant", answer))


# ---------- Tab 2: Quiz ----------
with tab_quiz:
    st.subheader("Test yourself on a topic")

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Topic to be quizzed on", placeholder="e.g. Democratic Values")
    with col2:
        num_q = st.number_input("Questions", min_value=2, max_value=10, value=5)

    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz from your course material..."):
            quiz = generate_quiz(topic, vector_store, num_questions=num_q)
        if quiz:
            st.session_state.current_quiz = quiz
            st.session_state.quiz_topic = topic
            st.session_state.quiz_answers = {}
        else:
            st.error("Could not generate a quiz. Try a different topic or fewer questions.")

    if "current_quiz" in st.session_state:
        quiz = st.session_state.current_quiz
        st.divider()

        for i, q in enumerate(quiz):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            choice = st.radio(
                "Choose one:",
                options=list(q["options"].keys()),
                format_func=lambda k, q=q: f"{k}. {q['options'][k]}",
                key=f"quiz_q_{i}",
                index=None,
            )
            st.session_state.quiz_answers[i] = choice
            st.write("")

        if st.button("Submit Quiz"):
            score = 0
            for i, q in enumerate(quiz):
                user_choice = st.session_state.quiz_answers.get(i)
                if user_choice == q["correct_answer"]:
                    score += 1
                else:
                    st.warning(
                        f"Q{i+1}: Correct answer was **{q['correct_answer']}** "
                        f"- {q.get('explanation', '')}"
                    )

            total = len(quiz)
            st.success(f"Your score: {score}/{total}")

            memory.save_quiz_score(STUDENT_ID, st.session_state.quiz_topic, score, total)
            status = "completed" if score / total >= 0.7 else "in_progress"
            memory.mark_topic(STUDENT_ID, st.session_state.quiz_topic, status=status)


# ---------- Tab 3: Study Plan ----------
with tab_plan:
    st.subheader("Generate a study schedule")

    col1, col2 = st.columns([3, 1])
    with col1:
        subject_for_plan = st.text_input("Focus area", value=selected_subject)
    with col2:
        num_days = st.number_input("Days", min_value=1, max_value=14, value=5)

    if st.button("Generate Study Plan"):
        with st.spinner("Building your study plan..."):
            plan = generate_study_plan(subject_for_plan, num_days, vector_store=vector_store)

        if plan:
            st.markdown(f"### Study Plan: {plan['subject']}")
            for day in plan["days"]:
                with st.expander(f"Day {day['day']}: {day['goal']}"):
                    for t in day["topics"]:
                        st.write(f"- {t}")
        else:
            st.error("Could not generate a study plan. Try again.")


# ---------- Tab 4: Progress ----------
with tab_progress:
    st.subheader("Your learning progress")

    topics = memory.get_topics(STUDENT_ID)
    weak_topics = memory.get_weak_topics(STUDENT_ID)

    st.markdown("**Topics covered:**")
    if topics:
        for topic, status in topics:
            icon = "✅" if status == "completed" else "🟡"
            st.write(f"{icon} {topic} ({status})")
    else:
        st.write("No topics tracked yet. Take a quiz to get started!")

    st.markdown("**Areas to review:**")
    if weak_topics:
        for topic, score, total in weak_topics:
            st.write(f"⚠️ {topic}: {score}/{total}")
    else:
        st.write("No weak areas identified yet.")

    recent = memory.get_recent_conversations(STUDENT_ID, limit=5)
    if recent:
        st.markdown("**Recent questions:**")
        for q, a in recent:
            st.write(f"- {q}")
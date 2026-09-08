# AI Learning & Study Assistant

## IBM SkillsBuild Internship (Agentic AI)

---

# 1. Project Overview

## 1.1 Project Title

**AI Learning & Study Assistant**

## 1.2 Problem Statement

Students often struggle to organize self-study around scattered course
material such as PDFs, lecture notes, and syllabi. They may have no easy
way to ask targeted questions, test their understanding, or plan revision
time.

Generic AI chatbots answer from general knowledge rather than the student's
actual syllabus, which can mislead exam preparation.

There is a need for a study companion that answers from a student's own
course material, remembers their learning history, and proactively helps
with revision.

## 1.3 Brief Description

The **AI Learning & Study Assistant** is a locally-run agentic AI system
that helps students study from their own uploaded course material.

It can:

- Answer questions based on uploaded study material
- Generate topic-wise quizzes
- Create day-by-day study plans
- Track learning progress
- Identify weak topics
- Remember previous interactions

The system combines three core agent capabilities:

- **Retrieval-Augmented Generation (RAG)**
- **Persistent Memory**
- **Tool Use**

The project uses open-source, locally hosted AI models through **Ollama**,
avoiding dependency on paid external APIs such as OpenAI.

---

# 2. Objectives & Proposed Solution

## 2.1 Project Objectives

- Build a Retrieval-Augmented Generation (RAG) pipeline that answers
  questions using the student's own course material.
- Add a persistent memory layer that tracks conversation history, topics
  covered, and quiz performance.
- Implement agent tools for quiz generation and study-plan generation.
- Reduce hallucinated answers using a similarity-score relevance threshold.
- Provide a simple multi-subject web interface.
- Run the AI locally using open-source models.
- Avoid paid external API dependencies.
- Keep student data stored locally.

## 2.2 How the Agentic AI Solution Works

The system follows a modular pipeline.

When a student uploads a course PDF:

1. The PDF is loaded and divided into overlapping text chunks.
2. The chunks are converted into embeddings using the local
   `nomic-embed-text` model through Ollama.
3. The embeddings are stored in a subject-specific ChromaDB vector store.
4. When the student asks a question, the system retrieves the most
   relevant chunks.
5. A similarity-score threshold checks whether the question is actually
   covered by the uploaded material.
6. If relevant content is found, the retrieved information is combined
   with recent conversation history and student learning information.
7. The local `qwen2.5:7b` model generates a grounded response.
8. Interactions and quiz performance are stored in SQLite memory.

The same retrieval system supports the quiz and study-plan tools.

### Quiz Generation

The assistant retrieves relevant course content and uses the local LLM to
generate multiple-choice questions, answers, explanations, and scores.

### Study Plan Generation

The assistant uses the available subject content to generate a
day-by-day revision schedule progressing from basic to advanced topics.

### Persistent Memory

Conversation history, topics covered, and quiz results are stored locally,
allowing the assistant to personalize future interactions.

---

# 2.3 Key Features

### Subject-grounded Q&A

Answers are generated using the uploaded course material rather than
general internet knowledge.

### Hallucination Guard

A relevance-score check helps prevent the assistant from answering
out-of-syllabus questions with fabricated information.

### Persistent Memory

The system remembers recent interactions and tracks weak topics.

### Automatic Quiz Generation

Generates topic-wise multiple-choice quizzes with explanations and
score tracking.

### Study Plan Generation

Creates a day-by-day revision plan based on the selected subject.

### Multi-subject Support

Students can upload and switch between multiple course subjects.

### Local AI

The application uses Ollama and locally hosted models.

**No OpenAI API key or paid OpenAI account is required.**

---

# 3. Implementation & Results

## 3.1 Technologies / Tools Used

| Component | Technology |
|---|---|
| LLM | Ollama (`qwen2.5:7b`) |
| Embeddings | Ollama (`nomic-embed-text`) |
| Vector Store | ChromaDB |
| Orchestration | LangChain |
| Memory Store | SQLite |
| Frontend | Streamlit |
| Language | Python 3.12 |
| AI Runtime | Ollama |

## 3.2 Key Agent Capabilities

| Capability | Implementation |
|---|---|
| RAG | Course PDFs are chunked, embedded, and stored in ChromaDB. Relevant chunks are retrieved before generating answers. |
| Memory | SQLite stores conversation history, topics covered, and quiz scores. |
| Tools | LLM-powered quiz and study-plan generation. |

---

# 3.3 Working Process

### Day 1

Selected the AI Learning & Study Assistant use case and configured the
Python 3.12 environment and local Ollama models.

### Day 2

Built the RAG pipeline including PDF loading, text chunking, embeddings,
and ChromaDB storage.

### Day 3

Added SQLite-backed conversation history, weak-topic tracking, and the
similarity-score guard.

### Day 4

Implemented the LLM-driven quiz generator and study-plan generator.

### Day 5

Built the Streamlit interface with chat, quiz, study-plan, and progress
features, together with multi-subject support and a custom visual theme.

---

# 3.4 Screenshot / Output

**Figure 1:** Home dashboard of the AI Learning & Study Assistant,
showing the subject selector and the "Ask a Question" interface.

Add screenshots of the working application here.

---

# 3.5 Results Achieved

- The RAG pipeline retrieves topic-specific information from uploaded
  course material.
- Questions related to the uploaded material receive grounded responses.
- Out-of-scope questions can be rejected using the relevance-score guard.
- The quiz generator creates multiple-choice questions with answer
  tracking and explanations.
- Quiz results are used to identify weak topics.
- The study-plan generator creates logically sequenced revision plans.
- Multiple subjects can be handled through the same interface.
- The system operates using locally hosted Ollama models without requiring
  an OpenAI API key.

---

# 4. Conclusion & Future Scope

## 4.1 Project Conclusion

The **AI Learning & Study Assistant** demonstrates a complete agentic AI
system combining RAG, memory, and tool use to solve a practical student
learning problem.

The project demonstrates key agentic AI concepts including:

- Grounding LLM responses in retrieved data
- Maintaining state across interactions
- Using callable tools
- Tracking student learning progress
- Reducing hallucinations through relevance checking

The complete system is implemented using open-source, locally hosted
technology through Ollama.

## 4.2 Challenges Faced

### Local LLM limitations

Smaller local LLMs may not always follow strict instructions to refuse
out-of-scope questions. Therefore, a code-level similarity-score guard is
used in addition to prompting.

### Source document quality

The quality of the uploaded document directly affects RAG performance.
Content-rich course material produces better results than PDFs containing
only topic lists or indexes.

### Library compatibility

Rapid changes in the LangChain ecosystem required adapting imports and
package usage during development.

---

# 4.3 Future Enhancements

- Multi-user support with individual login and progress tracking
- Support for PPTX and DOCX files
- Support for scanned/OCR PDFs
- Voice-based interaction
- Improved personalized learning recommendations
- Hosted deployment for larger-scale usage
- Cloud-based vector storage for scalability

---

# 4.4 References

- LangChain Documentation
- Ollama Documentation
- ChromaDB Documentation
- Streamlit Documentation
- Course material: Human Values and Ethics (GE3791), Unit I —
  Democratic Values

---

# 5. Installation & Setup

## Prerequisites

Before running the project, install:

- Python 3.12
- Ollama
- Git

## Install Python Dependencies

Clone the repository:

```bash
git clone https://github.com/GowriCherry31/AI-Student-Support-Assistant.git
cd AI-Student-Support-Assistant

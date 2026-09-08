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

It answers questions grounded in the student's course material, generates
topic-wise quizzes, builds day-by-day study plans, and tracks a student's
progress and weak areas over time.

The system combines three core agent capabilities:

- **Retrieval-Augmented Generation (RAG)**
- **Persistent Memory**
- **Tool Use**

The project uses open-source, locally hosted models through **Ollama**,
avoiding dependency on paid external APIs.

**No OpenAI API key is required.**

# 2. Objectives & Proposed Solution

## 2.1 Objectives

The main objectives of the AI Learning & Study Assistant are:

- Help students understand their own course material.
- Provide answers grounded in uploaded study materials.
- Reduce the risk of incorrect answers caused by relying only on general AI knowledge.
- Generate topic-wise quizzes for self-assessment.
- Create personalized study plans based on available learning material.
- Maintain persistent student memory such as learning history and weak areas.
- Demonstrate agentic AI concepts including RAG, memory, and tool usage.
- Run the complete system locally using open-source models through Ollama.
- Avoid dependency on paid external AI APIs.

## 2.2 Proposed Solution

The proposed solution is an **AI-powered learning assistant** that combines
Retrieval-Augmented Generation (RAG), persistent memory, and tool-based
actions into a single agentic workflow.

Students can provide their course materials, such as PDF notes and study
documents. The system processes these materials and stores their information
in a vector database.

When a student asks a question, the system retrieves the most relevant
information from the course material and provides a context-aware response
using a locally hosted Large Language Model (LLM).

The assistant can also perform additional learning tasks through tools, such
as generating quizzes and creating study plans. Student-related information
is stored using persistent memory so that the assistant can provide more
personalized support during future study sessions.

The complete workflow is designed to run locally using **Ollama**, with no
OpenAI API key or paid AI service required.

## 2.3 Proposed Architecture

The overall system follows this agentic workflow:

Student
   ↓
Streamlit User Interface
   ↓
AI Learning & Study Assistant
   ↓
┌─────────────────────────────────────┐
│           Agentic Workflow          │
├─────────────────────────────────────┤
│  1. RAG / Knowledge Retrieval       │
│  2. Persistent Student Memory       │
│  3. Tool Selection & Execution      │
│  4. Local LLM Response Generation   │
└─────────────────────────────────────┘
   ↓
Personalized Study Response

### RAG

The RAG pipeline retrieves relevant information from the student's uploaded
course materials before generating an answer. This helps keep responses
grounded in the available learning content.

### Persistent Memory

Student information and learning-related data are stored using SQLite-based
persistent memory. This allows the assistant to retain useful information
between sessions.

### Tool Use

The assistant can use dedicated tools for learning-related tasks, including
quiz generation and study-plan creation.

### Local AI

The language model runs locally through **Ollama**, allowing the project to
operate without requiring an OpenAI API key or paid external AI services.
# 3. Agentic AI Pipeline & Architecture

The AI Learning & Study Assistant follows an agentic workflow in which
different components work together to understand the student's request,
retrieve relevant information, use appropriate tools, and generate a useful
response.

## 3.1 Agentic Pipeline

The main workflow is:

Student Query
   ↓
Streamlit Interface
   ↓
AI Agent
   ↓
┌─────────────────────────────────────┐
│         Decision / Reasoning        │
│                                     │
│  • Understand the user's request    │
│  • Retrieve relevant material       │
│  • Check student memory             │
│  • Select required tools            │
└─────────────────────────────────────┘
   ↓
┌──────────────┬───────────────┬───────────────┐
│     RAG      │    Memory     │     Tools     │
│              │               │               │
│ Course       │ Student       │ Quiz          │
│ material     │ history       │ Study plan    │
│ retrieval    │ & progress    │ generation    │
└──────────────┴───────────────┴───────────────┘
   ↓
Local LLM through Ollama
   ↓
Final Personalized Response
   ↓
Student

## 3.2 Retrieval-Augmented Generation (RAG)

The RAG component allows the assistant to answer questions using information
from the student's course materials.

The process consists of:

1. Loading course documents.
2. Splitting the documents into smaller sections.
3. Generating embeddings for the document content.
4. Storing the embeddings in ChromaDB.
5. Retrieving the most relevant sections when a student asks a question.
6. Providing the retrieved context to the language model.
7. Generating a response based on the retrieved information.

This approach helps the assistant focus on the student's actual learning
materials instead of relying only on general model knowledge.

## 3.3 Persistent Student Memory

The assistant uses persistent memory to store useful student-related
learning information.

SQLite is used as the persistent storage layer.

The memory component can be used to maintain information such as:

- Previous learning interactions
- Topics studied
- Areas that need improvement
- Learning progress
- Other useful study-related information

Persistent memory allows the assistant to provide more personalized support
across multiple study sessions.

## 3.4 Tool Usage

The agent can use specialized Python tools for learning tasks.

Examples include:

- **Quiz Generation** — creates questions for testing understanding.
- **Study Plan Generation** — helps organize topics into a structured study
  schedule.
- **Learning Support** — performs task-specific processing instead of using
  the language model for every operation.

Tool usage demonstrates an important agentic AI concept: the assistant can
select and use external capabilities when they are more appropriate for the
user's request.

## 3.5 Local LLM Processing

The project uses **Ollama** to run the language model locally.

The intended LLM is:

**Qwen 2.5 7B**

The system also uses:

**nomic-embed-text**

for generating embeddings used by the RAG pipeline.

Because the models run locally through Ollama, the project does not require
an OpenAI API key or a paid external AI service.

## 3.6 System Architecture

The major components of the system are:

| Component | Purpose |
|-----------|---------|
| Streamlit | Provides the web-based user interface |
| Agent | Coordinates the learning workflow |
| RAG Pipeline | Retrieves relevant course material |
| ChromaDB | Stores and searches document embeddings |
| Ollama | Runs the local LLM and embedding model |
| SQLite | Stores persistent student memory |
| Python Tools | Performs quiz and study-plan tasks |
| Course Materials | Provides the student's learning knowledge base |

Together, these components create an agentic study assistant capable of
retrieving knowledge, maintaining memory, using tools, and generating
personalized responses.

# 4. Key Features

The AI Learning & Study Assistant provides the following major features:

## 4.1 Course Material-Based Question Answering

Students can ask questions related to their uploaded course materials.

The RAG pipeline retrieves relevant content from the knowledge base and uses
that context to generate an informative answer.

This helps students study from their own notes and course resources.

## 4.2 Retrieval-Augmented Generation

The system uses RAG to connect the local language model with the student's
learning materials.

Key steps include:

- Document loading
- Text processing and chunking
- Embedding generation
- Vector storage
- Similarity-based retrieval
- Context-aware answer generation

## 4.3 AI-Powered Quiz Generation

The assistant can generate topic-wise quizzes to help students test their
understanding.

Quizzes can be used for:

- Self-assessment
- Revision
- Practice before examinations
- Identifying topics that require additional study

## 4.4 Personalized Study Plans

The system can generate structured study plans to help students organize
their preparation.

A study plan can divide learning material into manageable topics and provide
a clear sequence for revision.

## 4.5 Persistent Student Memory

The assistant maintains persistent learning information using SQLite.

This allows useful student information to remain available between different
sessions instead of being lost when the application is restarted.

## 4.6 Local AI Processing

The project uses Ollama for local AI model execution.

This provides:

- No OpenAI API key requirement
- No paid OpenAI API usage
- Local model execution
- Greater control over the learning environment
- Ability to work without sending study material to an external AI API

## 4.7 Interactive Streamlit Interface

The application provides a simple web interface using Streamlit.

Students can interact with the assistant through the browser and access its
learning capabilities from a single interface.

## 4.8 Agentic AI Workflow

Instead of functioning only as a basic chatbot, the system combines:

- Reasoning and decision-making
- Knowledge retrieval
- Persistent memory
- Tool execution
- Local language-model generation

This demonstrates the core concepts of an **Agentic AI system**.

## 4.9 Student-Centric Learning Support

The overall system is designed around the student's learning process.

It combines course-material-based answers, quizzes, study planning, and
persistent memory to create a more useful and personalized study companion.

# 5. Technologies Used

The project is built using Python and open-source technologies for local
agentic AI development.

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Main programming language |
| Ollama | Runs AI models locally |
| Qwen 2.5 7B | Local Large Language Model |
| nomic-embed-text | Local embedding model |
| LangChain | Agent and AI workflow orchestration |
| LangChain Community | Document loaders and integrations |
| LangChain Ollama | Ollama model integration |
| ChromaDB | Vector database for RAG |
| SQLite | Persistent student memory |
| Streamlit | Web-based user interface |

---

# 6. Installation & Setup

## 6.1 Prerequisites

Before running the project, install the following:

- Python 3.12
- Git
- Ollama

The project is designed to run locally and does not require an OpenAI API key.

## 6.2 Clone the Repository

Open Git Bash or a terminal and run:

```bash
git clone https://github.com/GowriCherry31/AI-Student-Support-Assistant.git

## 6.2 Clone the Repository

Open Git Bash or a terminal and run:

```bash
git clone https://github.com/GowriCherry31/AI-Student-Support-Assistant.git
cd AI-Student-Support-Assistant
6.3 Create a Virtual Environment

Create a Python virtual environment:

python -m venv venv

Activate it on Windows using Git Bash:

source venv/Scripts/activate

If using Command Prompt instead:

venv\Scripts\activate
6.4 Install Python Dependencies

Install the required packages:

pip install -r requirements.txt
6.5 Install and Start Ollama

Install Ollama on your system and make sure the Ollama application is
running.

Check that Ollama is available:

ollama --version

Pull the language model:

ollama pull qwen2.5:7b

Pull the embedding model:

ollama pull nomic-embed-text

Verify the installed models:

ollama list

You should see the required models in the list.

6.6 Run the Application

After activating the virtual environment and starting Ollama, run:

streamlit run app.py

Streamlit will provide a local address in the terminal. Open that address
in your web browser to use the AI Learning & Study Assistant.

6.7 Important Note

The first model download can require significant disk space. The required
storage depends on the Ollama models being downloaded.

Once the models are downloaded, the application can use them locally without
requiring an OpenAI API key.

No paid OpenAI service is required for this project.



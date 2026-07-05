# NovaTech Enterprise Support Platform

An AI-powered enterprise customer support platform built using **LangGraph**, **Google Gemini**, **RAG (Retrieval-Augmented Generation)**, **ChromaDB**, and **Flask**.
The application routes customer requests to specialized AI agents, retrieves company policies from a vector database, maintains conversation state with SQLite, and provides a modern web interface.


https://github.com/user-attachments/assets/5911ee50-99b6-45c0-b636-54e688fa8a98

If the embedded player is unavailable, you can download the original recording here:
[demo.mp4](assets/demo.mp4)




## Features

- Multi-Agent Architecture using LangGraph
- Supervisor-based intelligent request routing
- Retrieval-Augmented Generation (RAG)
- Google Gemini integration
- ChromaDB vector database
- Persistent conversation memory using SQLite
- Enterprise policy retrieval
- Customer profile awareness
- Domain-restricted responses
- Modern Flask web interface
- Docker support
- LangSmith evaluation pipeline
- Modular and scalable architecture


## Architecture

```text
                        User
                         │
                         ▼
                  Flask Web Interface
                         │
                         ▼
                    Chat Service
                         │
                         ▼
                LangGraph Workflow
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 Supervisor        Retrieval Agent   Support Agent
        │                │
        │                ▼
        │         Retrieval Service
        │                │
        │                ▼
        │          Gemini Embeddings
        │                │
        │                ▼
        │            ChromaDB
        │
        ▼
 Escalation Agent

        ▼
 Unsupported Request Agent
```





# Tech Stack

### AI

- Google Gemini
- LangGraph
- LangSmith

### Retrieval

- ChromaDB
- RAG

### Backend

- Python
- Flask

### Database

- SQLite
- ChromaDB

### Deployment

- Docker
- Docker Compose



# Agent Workflow

## Supervisor Agent

Responsible for routing customer requests to the correct specialist.

Routes requests to:

- Support Agent
- Retrieval Agent
- Escalation Agent
- Unsupported Request Agent



## Support Agent

Handles:

- Greetings
- Subscription questions
- Account status
- General customer support conversations



## Retrieval Agent

Handles:

- Refund policy
- Enterprise support policy
- Account security
- Technical troubleshooting
- Product documentation

Uses:

- Gemini Embeddings
- ChromaDB
- Retrieval-Augmented Generation (RAG)



## Escalation Agent

Handles:

- Angry customers
- Human manager requests
- Serious complaints
- Legal threats



## Unsupported Request Agent

Politely rejects questions outside the scope of NovaTech customer support such as:

- Mathematics
- Programming
- History
- Sports
- Weather
- General knowledge



# Knowledge Base

The application indexes enterprise documents including:

- Company Policies
- FAQs
- Technical Documentation
- Enterprise Support Policies
- Account Security Policies

The indexing pipeline consists of:

```text
Documents
      │
      ▼
Document Loader
      │
      ▼
Document Chunker
      │
      ▼
Knowledge Builder
      │
      ▼
Gemini Embeddings
      │
      ▼
ChromaDB
```



# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/novatech-enterprise-support-platform.git

cd novatech-enterprise-support-platform
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```



## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY

LANGSMITH_API_KEY=YOUR_API_KEY

LANGSMITH_PROJECT=NovaTech_Support_Platform

LANGSMITH_TRACING=true
```



## 5. Build the Knowledge Base

Run once whenever the dataset changes.

```bash
python build_knowledge_base.py
```



## 6. Run the Application

```bash
python app.py
```

Open:

```
http://localhost:5000
```



# Docker

Build and run:

```bash
docker compose up --build
```

Open:

```
http://localhost:5000
```



# Evaluation

Run the LangSmith routing evaluation:

```bash
python -m src.evaluation.run_evaluation
```



# Example Questions

### Support

```
Hello
```

```
What is my subscription tier?
```



### Retrieval

```
What is the refund policy?
```

```
How do I recover my account?
```

```
My screen keeps flickering.
```



### Escalation

```
I want to speak to your manager.
```

```
I'm going to sue your company.
```



### Unsupported

```
What is 5 + 5?
```

```
Write a Python function.
```

# Learnings Folder

This folder is our reflection and documentation space for the project.

We built a full production-style agentic RAG system step by step, and along the way we learned many tools, concepts, workflows, and debugging patterns. Before moving further into quality tuning and product polish, this folder helps us pause and document what we have achieved properly.

## Purpose

The goal of this folder is to make our learning journey easy to revisit later.

It is useful for:

- understanding the tools and terminology in simple language
- remembering how the full pipeline works from start to finish
- revisiting the major errors and how we fixed them
- tracking what is already complete
- identifying what still remains for future improvement

## Files In This Folder

### 1. `01_tools_and_terminology.ipynb`

This notebook explains the important tools, concepts, and terminology used in the project in simple language.

It includes topics like:

- localhost
- ports
- Docker
- Docker Compose
- PostgreSQL
- OpenSearch
- BM25
- embeddings
- Jina
- Docling
- Ollama
- Airflow
- Redis
- Langfuse
- Telegram bot
- RAG
- hybrid search
- agentic RAG

This notebook is best for building strong conceptual understanding.

### 2. `02_project_workflow_end_to_end.ipynb`

This notebook explains the complete working pipeline of the project from beginning to end.

It covers:

- infrastructure setup
- service startup
- paper fetching
- PDF downloading
- PDF parsing
- PostgreSQL storage
- chunking
- embedding generation
- OpenSearch indexing
- hybrid retrieval
- normal RAG
- streaming RAG
- agentic RAG
- Telegram bot usage
- Langfuse monitoring and tracing

This notebook is best for understanding how the system actually works as one connected pipeline.

### 3. `03_errors_challenges_and_resolutions.ipynb`

This notebook documents the challenges we encountered and how we resolved them.

It includes:

- parsing issues
- async and sync mismatches
- missing system dependencies
- corrupted PDFs
- fallback parser support
- embedding rate limits
- OpenSearch storage and indexing problems
- old Docker image / rebuild problems
- tracing bugs
- Telegram bot conflicts
- Langfuse setup issues

This notebook is best for learning practical debugging and problem-solving from our real journey.

### 4. `PROGRESS_RECORD.md`

This file records the current state of the project in a concise way.

It answers:

- what is already complete
- what has been verified successfully
- what supporting integrations are working
- what is planned next

This file is the best quick status reference.

## Suggested Reading Order

If someone is new to the project, this order will be the most helpful:

1. `01_tools_and_terminology.ipynb`
2. `02_project_workflow_end_to_end.ipynb`
3. `03_errors_challenges_and_resolutions.ipynb`
4. `PROGRESS_RECORD.md`

Why this order:

- first understand the words and tools
- then understand the full flow
- then understand the real-world difficulties
- finally review the current project status and future direction

## What This Folder Represents

This folder is more than notes. It is evidence of the progress we made.

We did not just run a tutorial. We built, debugged, repaired, integrated, and validated a full system with many moving parts:

- databases
- search
- embeddings
- parsing
- retrieval
- answer generation
- tracing
- Telegram integration
- agentic workflows

That is a big achievement, and this folder helps preserve that learning in a useful way.

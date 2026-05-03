# Agentic RAG — arXiv Paper Curator

A production-grade RAG system built on arXiv CS.AI papers. Implements
hybrid search (BM25 + vector), local LLM generation via Ollama, Redis 
caching, Langfuse tracing, and an agentic LangGraph pipeline with 
guardrail validation, document grading, and adaptive query rewriting.

## Stack

| Component | Purpose |
|-----------|---------|
| FastAPI | REST API |
| PostgreSQL | Paper metadata storage |
| OpenSearch | BM25 + vector hybrid search |
| Ollama | Local LLM inference |
| Jina AI | Embeddings (1024-dim) |
| Redis | Response caching |
| Langfuse | Pipeline tracing and observability |
| Airflow | Automated ingestion DAG |
| LangGraph | Agentic workflow orchestration |

## How to Run

```bash
cp .env.example .env
# Add JINA_API_KEY to .env
docker compose up --build -d
```

See notebooks `01_` through `07_` for step-by-step verification.

## Status

End-to-end verification in progress. README will be updated with
real performance numbers after full pipeline run.

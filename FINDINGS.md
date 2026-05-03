# Extracted Findings from Original Notebooks

These are real outputs from executed cells in the original weekly notebooks.
To be used as baseline when writing new notebooks and verified against 
our own end-to-end run.

---

## 01 — Infrastructure (from week1)

### Environment check
```
Python Version: 3.12.11
Environment: /Users/Shared/Projects/MOAI/zero_to_RAG/.venv/bin/python
✓ Python version compatible
✓ Project root: /Users/Shared/Projects/MOAI/zero_to_RAG
```

### Tool versions
```
✓ Docker: Docker version 28.1.1, build 4eba377
✓ Docker Compose: v2.35.1-desktop.1
✓ UV: uv 0.7.13 (Homebrew 2025-06-12)
✓ All required software ready!
✓ Docker is running
```

### Container status (all 6 healthy)
```
SERVICE STATUS
======================================================================
Service              State           Status          Notes
----------------------------------------------------------------------
✓ airflow            running        healthy        Ready
✓ api                running        healthy        Ready
✓ opensearch-dashboards running        healthy        Ready
✓ ollama             running        healthy        Ready
✓ opensearch         running        healthy        Ready
✓ postgres           running        healthy        Ready
```

### FastAPI
```
✓ FastAPI is responding
Status: ok
```

### Airflow
```
✓ Airflow is healthy

Airflow Login:
URL: http://localhost:8080
Username: admin
Password: sBtDW9ffYBgETMqR
```

### OpenSearch Dashboards
```
✓ OpenSearch Dashboards is accessible!
✓ Web interface is ready for exploration

 Web Interface Access:
========================================
Main Dashboard: http://localhost:5601
Dev Tools: http://localhost:5601/app/dev_tools
========================================
```

### Ollama service
```
✓ Ollama is running!
Available models: 1

Installed Models:
  • llama3.2:1b (1.2 GB)

✓ Ollama API is healthy!
Version: 0.11.2
```

### Ollama model download
```
DOWNLOADING LLAMA 3.2:1B MODEL
==================================================
This is a small 1.3GB model - perfect for testing!
Download will take 2-5 minutes depending on your internet speed...
Llama 3.2:1b model downloaded successfully!
```

### LLM inference test (llama3.2:1b)
```
Testing llama3.2:1b with prompt: 'What is machine learning in one sentence?'
------------------------------------------------------------
Generating response (this may take 10-30 seconds)...
Response generated in 2.9 seconds

RESPONSE:
========================================
Machine learning is a subfield of artificial intelligence that enables
computers to learn from data, make predictions or decisions without being
explicitly programmed, by analyzing patterns and relationships within the data.
========================================

Model: llama3.2:1b
Generation time: 2929ms

SUCCESS! Your local AI model is working!
```

### PostgreSQL
```
✓ PostgreSQL is accepting connections on port 5432!

  Database Connection Details:
• Host: localhost
• Port: 5432
• Database: rag_db
• Username: rag_user
• Password: rag_password

✓ PostgreSQL connected
Found 46 total tables
Application tables: 1
Airflow tables: 45
  • papers
```

---

## 02 — Data Ingestion (from week2)

**No executed cell outputs.** Week 2 notebook cells contain code but no
saved outputs. The notebook was not executed before being committed.

---

## 03 — Keyword Search (from week3)

**No executed cell outputs.** Week 3 notebook cells contain code but no
saved outputs. The notebook was not executed before being committed.

---

## 04 — Hybrid Search (from week4)

**No executed cell outputs.** Week 4 notebook cells contain code but no
saved outputs. The notebook was not executed before being committed.

The notebook's Summary markdown cell documents expected performance targets
derived from prior development work (not from actual cell runs):

```
Search Performance Results (from summary docs, not executed outputs):
Method          Time (s)     Results    Notes
-------------------------------------------------
Client BM25     ~0.050s     53         Direct client
API BM25        ~0.150s     53         Production endpoint
Client Vector   ~0.005s     5          Direct client + embeddings
API Hybrid      ~2.500s     1-5        Production with RRF fusion

Expected chunks indexed: 81 chunks from 3 research papers
Embedding model: jina-embeddings-v3, dimension: 1024
Hybrid fusion weights: 60% BM25 + 40% vector (RRF)
```

### ⚠️ Security Note
Hardcoded Jina API key found in cell 2. Key has been rotated.
Line replaced with `os.environ["JINA_API_KEY"] = os.getenv("JINA_API_KEY", "")`

---

## 05 — RAG Pipeline (from week5)

### Environment
```
Python Version: 3.12.11
Project root: /Users/Shared/Projects/MOAI/zero_to_RAG
✓ Environment setup complete
```

### Service health
```
WEEK 5 SERVICE HEALTH CHECK
========================================
✓ FastAPI: Healthy
✓ OpenSearch: Healthy
✓ Ollama: Healthy

✓ All services ready for Week 5!
```

### Ollama model
```
OLLAMA LLM TEST
====================
Available models: 1
  • llama3.2:1b
```

### LLM sanity test
```
Testing LLM Generation:
✓ LLM responded: '8'
✓ Ollama is working!
```
(Prompt: "What is 2+6? Answer with just the number.")

### Search test
```
SEARCH TEST
===============
Searching for: 'machine learning'
✓ Found 3 results
✓ Search mode: hybrid

Top results:
  1. Improving Low-Resource Translation with Dictionary-Guided Fi... (score: 0.016)
  2. Deep Active Learning for Lung Disease Severity Classificatio... (score: 0.016)
```

### API endpoints
```
API STRUCTURE
====================
Total endpoints: 4

Available endpoints:
  • /api/v1/ask
  • /api/v1/health
  • /api/v1/hybrid-search/
  • /api/v1/stream
```

### Standard RAG (non-streaming)
```
COMPLETE RAG PIPELINE TEST (OPTIMIZED)
========================================
Question: Summarize machine learning papers?

✓ Success! (7.7 seconds)

Answer:
----------------------------------------
machine learning papers often focus on developing and applying techniques
from various domains to achieve specific goals, such as image classification,
natural language processing, or regression.
----------------------------------------

Sources: 1 papers
Chunks used: 1
Search mode: hybrid
```

### Streaming RAG
```
COMPLETE RAG PIPELINE TEST (STREAMING)
========================================
Question: Summarize machine learning papers?

Streaming response...
First response in: 3.7 seconds

Answer:
----------------------------------------
Here's a summary of relevant machine learning papers from arXiv:

Machine Learning Papers
=====================

Several studies have contributed to the field of machine learning, with
notable works including:

* Deep Active Learning for Lung Disease Severity Classification from Chest
  X-rays: Learning with Less Data in the Presence of Class Imbalance
  (arXiv:2508.21263v1)
    + This paper applied deep active learning with a Bayesian Neural Network
      (BNN) approximation and weighted loss function to reduce labeled data
      requirements for lung disease severity classification.
* Semi-Supervised Deep Learning for Activity Recognition (arXiv:2009.04466v2)
    + This study employed a semi-supervised approach, leveraging both labeled
      and unlabeled data to improve activity recognition accuracy.

Key Concepts
=============

* Deep Active Learning: an active learning strategy that selects samples with
  the highest confidence predictions from a model.
* Bayesian Neural Networks (BNNs): probabilistic neural networks that
  incorporate Bayesian inference for uncertainty estimation.
* Semi-Supervised Learning: using both labeled and unlabeled data to improve
  model performance.
...
----------------------------------------

✓ Complete! (Total: 21.0 seconds)

Sources: 1 papers
  1. https://arxiv.org/pdf/2508.21263.pdf
Chunks used: 1
Search mode: hybrid
```

### System status
```
SYSTEM STATUS SUMMARY
=========================
Overall Status: OK
Version: 0.1.0

Service Status:
  • database: healthy - Connected successfully
  • opensearch: healthy - Index 'arxiv-papers-chunks' with 511 documents
  • ollama: healthy - Ollama service is running

RAG Pipeline Status:
  ✓ Data Ingestion: Papers indexed in OpenSearch
  ✓ Search: BM25 + Vector hybrid search working
  ✓ LLM Generation: Ollama generating answers
  ✓ Performance: 6x speed improvement (120s → 15-20s)
  ✓ API: Clean endpoints ready for production

Endpoint Status:
  ✓ Standard RAG: /api/v1/ask/ (working)
  ⚠ Streaming RAG: /api/v1/ask/ask-stream/ (needs container rebuild)
  ✓ Search: /api/v1/hybrid-search/ (working)

🎉 Complete RAG system operational!
```

### Gradio
```
✅ Gradio interface is running!
   Visit: http://localhost:7861
```

---

## 06 — Monitoring and Caching (from week6)

### Service health (all 5 healthy including LangFuse and Redis)
```
WEEK 6 SERVICE HEALTH CHECK
========================================
✓ FastAPI: Healthy
✓ OpenSearch: Healthy
✓ Ollama: Healthy
✓ LangFuse: Healthy

Checking Redis:
ℹ Redis: Not in health endpoint, checking direct connection...
✓ Redis: Healthy (direct connection)

✓ All services ready for Week 6!
```

### API structure (unchanged from week5)
```
API STRUCTURE
====================
Total endpoints: 4

Available endpoints:
  • /api/v1/ask
  • /api/v1/health
  • /api/v1/hybrid-search/
  • /api/v1/stream
```

### Cache configuration
```
CACHE CONFIGURATION
========================================
API Status: ok
Cache Integration: Built into RAG endpoints
Cache Type: Redis
Cache Strategy: Exact parameter matching
TTL: Configurable (default 24 hours)

✓ Cache system is integrated and ready
```

### First query (labelled "no cache" — likely already cached)
```
FIRST QUERY TEST (NO CACHE - BASELINE)
==================================================
Query: What are the latest advances in transformer models for NLP?

✓ Success!
Response Time: 0.24 seconds

Answer Preview:
--------------------------------------------------
Transformer models have made tremendous progress in recent years, with
significant advancements in language understanding and generation. One area
of focus is the development of more efficient quantization techniques to
improve model deployment on consumer hardware. The latest research highlights
the importance of learning-based orthogonal butterfly transforms
(ButterflyQuant) for ultra-low-bit la...
--------------------------------------------------

Metadata:
  • Sources: 2 papers
  • Chunks used: 3
  • Search mode: hybrid

📊 Baseline established: 0.24 seconds
```

**Interpretation:** 0.24 seconds is far too fast for a full LLM generation
pass. The cache was already warm from a prior notebook run; Redis was not
flushed before the test. This is not a true cold-start baseline.

### Second query (cache hit confirmed)
```
SECOND QUERY TEST (WITH CACHE - OPTIMIZED)
==================================================
Query: What are the latest advances in transformer models for NLP?

✓ Success!
Response Time: 0.131 seconds (131ms)

📊 PERFORMANCE COMPARISON
==================================================
First Query (no cache): 0.24 seconds
Second Query (cached): 0.131 seconds

🚀 Speed Improvement: 2x faster
⏱️ Time Saved: 0.10 seconds

✓ Answers are identical (cache working correctly)
```

### ⚠️ Measurement Note
The "cache miss" baseline of 0.24s is invalid — Redis was not flushed
before the test, so it was likely a cache hit. Real cold-start baseline
requires running `redis-cli FLUSHALL` before the first query.
Our run will establish the real numbers.

---

## 07 — Agentic RAG (from week7)

**No executed cell outputs.** Week 7 notebook cells contain code but no
saved outputs. The notebook was not executed before being committed.

---

## Summary of Key Numbers

| Metric | Value | Source |
|--------|-------|--------|
| Python version | 3.12.11 | Week 1 |
| Docker version | 28.1.1 | Week 1 |
| Docker Compose | v2.35.1-desktop.1 | Week 1 |
| UV version | 0.7.13 | Week 1 |
| Ollama version | 0.11.2 | Week 1 |
| LLM model in use | llama3.2:1b (1.2 GB) | Week 1 |
| LLM generation time (short prompt) | 2929ms (2.9s) | Week 1 |
| PostgreSQL tables total | 46 (1 app + 45 Airflow) | Week 1 |
| Application DB tables | 1 (papers) | Week 1 |
| OpenSearch index name | arxiv-papers-chunks | Week 5 |
| OpenSearch document count | 511 chunks | Week 5 |
| Hybrid search score ("machine learning") | 0.016 | Week 5 |
| Standard RAG latency (end-to-end) | 7.7 seconds | Week 5 |
| Streaming: time to first token | 3.7 seconds | Week 5 |
| Streaming: total response time | 21.0 seconds | Week 5 |
| API endpoint count | 4 | Week 5, 6 |
| Cache hit latency (observed) | 131ms | Week 6 |
| Cache "miss" latency (pre-warmed) | 240ms | Week 6 |
| Observed cache speedup | ~2x (pre-warmed artifact) | Week 6 |
| Claimed cold-start RAG latency | 120+ seconds (pre-optimization) | Week 5 docs |
| Claimed optimized RAG latency | 15–20 seconds | Week 5 docs |
| Claimed cache speedup | 150–400x | Week 6 docs |
| Jina embedding model | jina-embeddings-v3, 1024-dim | Week 4 docs |
| Hybrid fusion ratio | 60% BM25 + 40% vector (RRF) | Week 4 docs |
| LangFuse URL | http://localhost:3000 | Week 6 |
| Gradio URL | http://localhost:7861 | Week 5 |
| Airflow URL | http://localhost:8080 | Week 1 |
| OpenSearch Dashboards URL | http://localhost:5601 | Week 1 |

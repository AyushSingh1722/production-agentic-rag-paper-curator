# Progress Record

This file records what we have completed successfully so far, what is working right now, and what we plan to improve next.

## Project Status

Current status:

- core implementation is complete
- major integrations are working
- end-to-end pipeline has been validated
- remaining work is mostly quality refinement, polish, and product-facing improvements

## What We Have Successfully Completed

### 1. Infrastructure And Service Setup

We successfully set up and used the core services required by the project:

- Docker
- Docker Compose
- FastAPI service
- PostgreSQL
- OpenSearch
- Redis
- Ollama
- Airflow
- Langfuse
- Telegram bot service

We also learned how to work with:

- containers
- images
- ports
- localhost
- environment variables
- service health checks
- rebuild and restart workflows

### 2. API, REST Endpoints, And Client Layer

We successfully implemented the main application layer using FastAPI.

This includes working REST endpoints for:

- `/health`
- `/hybrid-search`
- `/ask`
- `/stream`
- `/ask-agentic`
- `/feedback`

We also already touched and implemented:

- FastAPI app setup
- router structure
- response models
- streaming responses
- async request handling
- Gradio interface code for a UI-based client

Important clarification:

- FastAPI is not a future feature; it is already implemented and used as the main backend
- REST endpoints are not pending from scratch; they already exist and are working
- Gradio is not untouched; it was implemented earlier, though it may still need future re-validation and polish
- async support is already part of the current system, especially in API handling, model calls, embeddings, and streaming

### 3. Data Ingestion Pipeline

We successfully implemented and verified the ingestion workflow:

- fetching papers
- downloading PDFs
- storing metadata
- processing multiple papers in the pipeline

This part is no longer just scaffolded. It has been run and validated.

### 4. PDF Parsing Pipeline

We successfully implemented and stabilized parsing:

- Docling parser integration
- async wrapper handling
- long PDF truncation strategy
- retry and redownload logic for corrupted cached PDFs
- fallback parser support when Docling fails

This was one of the hardest parts and is now working.

### 5. Database Storage

We successfully store parsed paper metadata and text in PostgreSQL.

This includes:

- paper metadata
- parsed raw text
- processed state tracking

### 6. Indexing Pipeline

We successfully completed and verified indexing:

- text chunking
- embedding generation using Jina
- OpenSearch indexing
- hybrid index verification

We also solved:

- Jina rate limit problems with retry and backoff
- OpenSearch write blocks caused by disk watermark issues

### 7. Retrieval Layer

We successfully implemented and verified:

- BM25 search
- hybrid search
- OpenSearch-backed retrieval

This means retrieval is no longer theoretical. It has been tested with real indexed papers.

### 8. Normal RAG

We successfully implemented and verified:

- `/ask`
- `/stream`

This includes:

- retrieval from OpenSearch
- context assembly
- answer generation using Ollama
- source return in the response

### 9. Agentic RAG

We successfully implemented and verified:

- `/ask-agentic`
- graph-based retrieval and reasoning flow
- document grading
- grounded answer generation
- reasoning step return
- trace ID return

We also fixed:

- dependency wiring issues
- source propagation issues
- chunk counting issues
- trace return issues

### 10. Telegram Bot

Telegram bot support is working.

We successfully:

- configured the bot token
- started the bot
- resolved multi-worker polling conflicts
- moved to a dedicated Telegram bot service pattern

### 11. Langfuse Monitoring And Tracing

Langfuse is working.

We successfully:

- brought up the Langfuse UI
- fixed environment configuration
- initialized tracing from the API
- generated traces
- returned trace IDs in agentic responses

This means observability is now in place.

## What Is Working Right Now

The following are currently working successfully:

- infrastructure startup
- FastAPI backend
- REST endpoints
- response schemas
- streaming endpoint support
- async request handling
- ingestion
- PDF parsing
- PostgreSQL persistence
- chunking
- Jina embeddings
- OpenSearch indexing
- BM25 and hybrid retrieval
- `/ask`
- `/stream`
- `/ask-agentic`
- Gradio client codebase
- Telegram bot
- Langfuse tracing

## Important Things We Learned

Some of the biggest practical learnings from this project were:

- many “simple” integration problems are really environment and orchestration problems
- Docker rebuilds matter when code changes are not reflected in a running container
- async and sync mismatches can quietly break a pipeline
- parser robustness matters more than happy-path assumptions
- search systems can fail because of infrastructure issues like disk limits, not only code bugs
- observability tools like Langfuse become much more useful after the main pipeline is working
- agentic workflows need extra grounding care to avoid drift and hallucination

## Planned Future Work

The main implementation is complete, but there is still valuable future work to do.

### 1. Quality Refinement

We want to improve:

- grounding quality
- answer precision
- citation style consistency
- source trustworthiness
- hallucination reduction
- comparison between normal RAG and agentic RAG

### 2. Evaluation Framework

We should create a small evaluation setup for the indexed dataset:

- benchmark questions
- expected answer patterns
- retrieval quality checks
- `/ask` versus `/ask-agentic` comparison
- Langfuse-assisted inspection of traces

### 3. Client Interface Refinement

The client interface layer has already been touched, but it can be improved further.

Current situation:

- FastAPI already works as the main backend interface
- REST endpoints already exist and are actively used
- Gradio interface code already exists

Future improvements may include:

- re-validating the Gradio interface against the latest backend changes
- making the Gradio UI more polished for demos
- easier interactive query testing
- clearer display of answers, sources, and reasoning traces

### 4. FastAPI And REST Endpoint Refinement

FastAPI and the REST layer are implemented, but we can still improve them.

Future improvements include:

- clearer endpoint documentation
- request and response examples
- stronger schema clarity
- better error response formatting
- easier developer onboarding for API consumers

### 5. Async Support Refinement

Async support is already present in important parts of the system, but it can still be made cleaner.

Potential improvements include:

- cleaner async boundaries
- better async consistency across services
- improved streaming and background task handling
- more predictable async behavior in integrations

### 6. Search And Index Quality Improvements

Possible future improvements:

- filter low-value chunks such as bibliography-heavy text
- refine chunking strategy
- improve hybrid ranking quality
- better relevance selection before answer generation

### 7. Deployment And Hardening

Future production-focused improvements may include:

- more polished deployment documentation
- stronger secret management practices
- reducing startup noise
- better health monitoring and service ownership documentation

## Big Picture Reflection

This project has already moved far beyond an initial prototype.

We have successfully built and validated a real multi-service system that includes:

- ingestion
- parsing
- storage
- indexing
- retrieval
- RAG
- agentic RAG
- Telegram access
- tracing and observability

That is a major milestone.

The next phase is not “can we build it?”

The next phase is:

- how do we make it cleaner
- how do we make it more accurate
- how do we make it easier to use
- how do we make it easier to evaluate

That is a very good place for the project to be in.

# Architecture Document: Memora AI

## Overview
Memora AI is a Developer Productivity Tool designed as a continuous, automated Project Memory Engine. It passively captures context through an IDE extension and allows querying of that context via an AI interface.

## Tech Stack
- **Frontend / Client:** 
  - VS Code Extension (TypeScript)
  - Next.js Web Dashboard
- **Backend:** Python (FastAPI)
- **Database:** PostgreSQL with `pgvector` for vector similarity search.
- **AI Models:** OpenAI API (configurable via environment variables, designed to support fallback endpoints like NVIDIA Build or OpenRouter if rate-limited).
- **Tooling:** GitHub Spec Kit, Playwright (for E2E tests), pytest (for backend).

## Data Model
- **DocumentChunk:** Stores semantic text chunks, metadata (source file, commit hash, timestamp), and `pgvector` embeddings.
- **KnowledgeEntry:** Represents manually uploaded sources (PDFs, docs) parsed and indexed.
- **User:** Authentication and authorization.

## High-Level Design
1. **Event Capture (VS Code Extension):** Listens to `onDidSaveTextDocument` and Terminal events, formatting them and pushing them over REST to the backend.
2. **Telemetry Ingestion (Backend):** `endpoints/telemetry.py` receives the raw events.
3. **Processing & Indexing:** `services/rag.py` processes textual diffs/logs into vector embeddings and stores them in PostgreSQL.
4. **Retrieval (Two-Tier RAG):** 
   - **Tier 1:** User queries are matched against `pgvector`. Only top matches (>0.75 similarity) are appended to a strict prompt instructing the LLM to exclusively use project evidence.
   - **Tier 2:** If no relevant project evidence is found, the system checks if it is a general programming question and provides a generic response tagged with `[General Explanation]`. Otherwise, it explicitly admits a lack of context.

## Day 2 Readiness
The architecture decouples the event source (VS Code) from the memory engine (FastAPI/pgvector). This allows us to easily ingest arbitrary new data sources, plug in different UI clients, or change retrieval strategies without systemic refactoring.

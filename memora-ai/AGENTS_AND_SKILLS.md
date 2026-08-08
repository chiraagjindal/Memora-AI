# Agents and Skills

## Custom Agents

### 1. Memora RAG Agent
**Description:** A strict, non-hallucinating AI agent integrated into the FastAPI backend (`backend/app/services/rag.py`).
**Role:** Receives queries via the VS Code Webview and routes them against the `pgvector` database to extract project evidence.
**Rules:** 
- MUST strictly cite "Source ID" if project evidence is found.
- MUST explicitly reply "I don't know" if project evidence is missing for a project-specific query.
- May fallback to `[General Explanation]` ONLY for general software engineering inquiries.

## Custom Skills

### 1. Semantic Telemetry Parser
**Description:** A parsing skill executed at the API edge (`telemetry.py`) to classify incoming VS Code events.
**Role:** Maps low-level IDE events (like `npm run dev`) into semantic project events ("Local Server Started") before generating embeddings for the vector database.

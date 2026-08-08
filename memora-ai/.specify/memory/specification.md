# Memora AI Specification

## Product Overview
Memora AI is a VS Code extension and Python backend that acts as an automated Project Memory Engine. It passively captures context while a developer works and provides an AI chatbot interface (NotebookLM style) to accurately answer questions about the project history and context without hallucinating.

## User Stories & Acceptance Criteria

### US-1: Context Capture
**As a** developer,
**I want** my IDE to automatically record my actions (file saves, git commits, terminal commands)
**So that** I don't have to manually document my engineering process.

**Acceptance Criteria:**
- VS Code extension activates on startup.
- Listens to `onDidSaveTextDocument` and sends the file path and content to the backend.
- Hooks into the terminal to log executed commands.
- Monitors Git commits to record commit messages and diffs.

### US-2: Document Uploads
**As a** developer or admin,
**I want** to manually upload external sources (PDFs, docs, links)
**So that** the AI can reference external project constraints and specs.

**Acceptance Criteria:**
- Backend provides a REST API to ingest files.
- Files are parsed, chunked, and embedded into the vector database (pgvector).

### US-3: Accurate Q&A (Strict RAG)
**As a** team member,
**I want** to ask questions about the project and receive highly accurate answers
**So that** I can understand decisions without being misled by AI hallucinations.

**Acceptance Criteria:**
- The Webview UI provides a chat interface.
- Project-specific queries only use retrieved context (pgvector).
- If no context is found, the AI explicitly replies "I don't know".
- General SWE queries are tagged as "General Explanation".

## Non-Functional Requirements
- **Performance:** Context capture must be non-blocking in the IDE.
- **Accuracy:** The RAG pipeline prioritizes precision over recall.
- **Hackathon Compliance:** The repository must contain all Deploy or Die mandatory checkpoints.

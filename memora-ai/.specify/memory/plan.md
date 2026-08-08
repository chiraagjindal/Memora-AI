# Memora AI - Hackathon Execution Plan (Deploy or Die)

This document is the official engineering execution plan for Memora AI, tailored for strict compliance with the **Deploy or Die Hackathon** requirements.

## 1. Goal Description & Track Alignment
**Track Alignment:** Track B (Developer Productivity Tools)
**Project Vision:** Memora AI is an AI-integrated project logger that captures the "memory" of a project automatically. A VS Code extension will capture engineering events (File Saves, Git Commits, Terminal Execution) and send them to our Python backend (PostgreSQL + pgvector). Developers can manually upload sources. The AI features a two-tier Retrieval-Augmented Generation (RAG) policy to answer questions accurately without fabricating project history.

## 2. Agent-Driven Lifecycle (ADLC) Workflow
We will use the **GitHub Spec Kit** and strictly follow a human-in-the-loop ADLC process. We will NOT use blind, unreviewed auto-generation.

### Initialization
1. Install Spec Kit: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
2. Initialize: `specify init memora-ai`

### The Five Linear Commands (Execution Order)
1. `/speckit.constitution`: Generate the rules and constitution file.
2. `/speckit.specify`: Create the PRD with user stories and acceptance criteria.
3. `/speckit.plan`: Generate the architecture document and technical plan.
4. `/speckit.tasks`: Break down the plan into manageable, trackable tasks.
5. `/speckit.analyze`: Run a read-only consistency check to verify alignment.
6. `/speckit.implement`: Execute the implementation while committing progressively.

## 3. The Five Non-Negotiables (Mandatory Checkpoints)
If any of these are missing, the submission will not be evaluated.

- [ ] **Architecture Document:** Create `ARCHITECTURE.md` describing our stack (Next.js, FastAPI, PostgreSQL/pgvector), data model, and high-level modular design. It must be designed for change to handle the Day 2 surprise requirement.
- [ ] **Agent Rules:** Create `.clinerules` and `AGENTS.md`. This will tightly manage agent context to survive rate-limits.
- [ ] **Working Code:** The application (VS Code extension + Python Backend) must build and run cleanly.
- [ ] **Custom Agent and Skill:** We will build at least one custom agent and one custom skill, explicitly documented in `AGENTS_AND_SKILLS.md`.
- [ ] **Green CI/CD Pipeline:** A GitHub Actions workflow (`.github/workflows/main.yml`) that builds the project and runs the test suite. The most recent run MUST pass.

## 4. Group Two Requirements (Scoring Criteria)
These criteria define our final score and are treated as required.

- [ ] **Specification / PRD:** Documented clearly (`PRD.md`), mapping user stories against acceptance criteria.
- [ ] **Playwright E2E Tests:** End-to-end tests for the webview/frontend passing in CI, with the HTML report uploaded as an artifact in GitHub Actions.
- [ ] **Code Quality Configuration:** Enforce linting (`ruff` for Python, `eslint` for TS) and static analysis via pre-commit hooks.
- [ ] **Clean, Progressive Commit History:** We will commit continuously and frequently. A single end-of-day commit dump is explicitly forbidden.
- [ ] **Task Breakdown:** The explicit plan the agent worked through (`tasks.md`).
- [ ] **Tagged Release:** We will use semantic versioning and cut a final GitHub Release (e.g., `v1.0.0`) at the end of Day 1.

## 5. System Architecture & Features
*Maintaining the established Memora AI vision.*

### VS Code Extension (Client)
- Captures File Saves, Git Commits, and Terminal Execution Logs.
- Acts as a UI (Webview) for the AI chat interface.

### Python Backend (FastAPI + pgvector)
- **REST Endpoints:** Ingests telemetry and uploaded files.
- **Two-Tier RAG Policy:** 
  1. *Project Evidence:* Strict pgvector queries with explicit citations for project-specific questions. Gracefully handles missing info with "I don't know".
  2. *General Explanation:* Uses the base model for general programming questions, tagged explicitly.

## 6. Testing and Verification Strategy
*This protects the project on Day 2.*
- **Backend Tests:** `pytest` to assert the strictness of the two-tier RAG policy.
- **Frontend/Extension Tests:** Playwright for E2E user flow verification.
- All tests will run automatically on push via GitHub Actions.

## 7. Submission Checklist
Alongside the public GitHub repo link, we will submit:
- [ ] Confirmation that the CI pipeline is green.
- [ ] Confirmation that Playwright tests pass.
- [ ] A ~3-minute demo video or comprehensive screenshots of the working app.

<!-- Sync Impact Report
- Version: 1.0.0
- Added sections: Core Principles, Development Guidelines
- Removed sections: N/A
-->
# Memora AI Constitution

## Core Principles

### I. Human-in-the-Loop ADLC (NON-NEGOTIABLE)
Blind, unreviewed auto-generation is strictly prohibited. Every agent action must be reviewed and approved by a developer. Code is written progressively with explicit understanding of intent.

### II. Accuracy Over Completeness (No Hallucinations)
Memora AI serves as a truthful Project Memory Engine. Project-specific questions MUST ONLY be answered using explicitly verified project evidence. If evidence is lacking, the system MUST state "I don't know". General knowledge can only be used if distinctly tagged as a "General Explanation".

### III. Progressive Versioning & Continuous Commits
All development must occur with clean, progressive commit histories. Giant end-of-day commit dumps are forbidden. Every logical milestone or component must be committed and pushed frequently.

### IV. Demonstrable & Validatable
Everything implemented must be observable and executable. If a feature or RAG pipeline cannot be run, traced, or verified by a judge during review, it does not count. Testable interfaces (CLI, API, Webview) are required.

### V. Modular Architecture for Day 2 Readiness
The architecture must remain decoupled (IDE Extension -> Memory Engine -> Vector DB). Tight coupling is forbidden to ensure that the system can seamlessly integrate the Day 2 surprise requirement without breaking existing features.

## Development Workflow

- All changes MUST start from the GitHub Spec Kit lifecycle (`/speckit.specify` → `/speckit.plan` → `/speckit.tasks`).
- Pre-commit hooks (`ruff`, `eslint`) MUST pass before merging.
- Playwright E2E and pytest backend tests MUST remain green in CI.

## Governance

This constitution supersedes all other practices and unreviewed AI suggestions. Any deviations require an explicit architectural decision record (ADR/Decision Card). The CI/CD pipeline is the ultimate arbiter of code quality and build health.

**Version**: 1.0.0 | **Ratified**: 2026-08-08 | **Last Amended**: 2026-08-08

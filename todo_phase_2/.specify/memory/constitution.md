<!--
Sync Impact Report:
Version change: N/A → 1.0.0 (initial version for Phase 2)
List of modified principles:
- Added "UV Dependency Management": All Python dependencies and commands must use uv. Commit uv.lock. No pip/poetry/pdm.
- Added "Core Logic Reuse": Business logic remains in domain/, app/use_cases.py, and infra/repo.py. Routes stay thin.
- Added "Cookie-Based Authentication": FastAPI authenticates users and issues auth session/JWT. FastAPI sets auth cookie via Set-Cookie. Cookie must be HttpOnly (and Secure in production). Frontend must NOT store tokens in localStorage/sessionStorage.
- Added "User Isolation": user_id is derived only from verified cookie/session. user_id must never be accepted from client request payloads.
- Added "Neon Postgres Persistence": Replace in-memory repo with Postgres repo only. No business logic duplication.
- Added "API Versioning": All endpoints under /api/v1.
Added sections:
- "Type Checking and Linting" section: No tests required. Provide: uv run ruff check . and uv run mypy src
- "Development Workflow" section: Follow Spec-Driven Development (SDD) methodology with Prompt History Records (PHRs) for all user interactions and Architectural Decision Records (ADRs) for significant decisions.
Removed sections: None
Templates requiring updates:
- ✅ plan-template.md - Constitution Check section exists but is generic, no specific changes needed
- ✅ spec-template.md - No specific constitution references to update
- ✅ tasks-template.md - No specific constitution references to update
- ✅ All templates checked, no specific updates required
Follow-up TODOs: None
-->
# Speckit Todo App - Phase 2 (FastAPI Auth + Cookies + Neon) Constitution

## Core Principles

### UV Dependency Management
All Python dependencies and commands must use uv. Commit uv.lock. No pip/poetry/pdm.

### Core Logic Reuse
Business logic remains in domain/, app/use_cases.py, and infra/repo.py. Routes stay thin.

### Cookie-Based Authentication
FastAPI authenticates users and issues auth session/JWT. FastAPI sets auth cookie via Set-Cookie. Cookie must be HttpOnly (and Secure in production). Frontend must NOT store tokens in localStorage/sessionStorage.

### User Isolation
user_id is derived only from verified cookie/session. user_id must never be accepted from client request payloads.

### Neon Postgres Persistence
Replace in-memory repo with Postgres repo only. No business logic duplication.

### API Versioning
All endpoints under /api/v1.

## Type Checking and Linting
No tests required. Provide: uv run ruff check . and uv run mypy src

## Development Workflow
Follow Spec-Driven Development (SDD) methodology with Prompt History Records (PHRs) for all user interactions and Architectural Decision Records (ADRs) for significant decisions.

## Governance
Constitution supersedes all other practices. Amendments require documentation and migration plan. All PRs/reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-05 | **Last Amended**: 2026-01-05

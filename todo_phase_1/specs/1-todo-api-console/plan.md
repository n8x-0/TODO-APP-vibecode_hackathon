# Implementation Plan: Todo API Console

**Branch**: `N/A` | **Date**: 2025-12-27 | **Spec**: specs/1-todo-api-console/spec.md
**Input**: Feature specification from `/specs/1-todo-api-console/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a Todo application consisting of a FastAPI backend with in-memory storage for CRUD operations and an interactive console client that communicates with this backend. The primary objective is to deliver a functional API-first Todo system for Phase I, adhering to defined architectural layers and coding principles.

## Technical Context

**Language/Version**: Python 3.11+ (as per common practice for FastAPI, and implicitly in the project context)
**Primary Dependencies**: FastAPI (for API backend), `httpx` or `requests` (for console client to call API), `uvloop` (for FastAPI performance), `uv` (as per constitution) 
**Storage**: In-memory (Python dictionaries/lists, as per Phase I scope in constitution)
**Testing**: `pytest` (for unit/integration tests of API logic), `ruff` (linting), `mypy` (type checking) (as per constitution, although tests are not explicitly 'required', `pytest` would be the standard framework if used. The constitution states "No tests required" for the overall project, but `pytest` would be used if any tests were to be written for specific components.) 
**Target Platform**: Linux server (for FastAPI backend), Cross-platform console environment (for client)
**Project Type**: Single project (monorepo structure with backend API and console client in distinct directories)
**Performance Goals**: API responses within 200ms (p95) for CRUD operations. Console startup within 5 seconds.
**Constraints**: In-memory storage only (no database persistence in Phase I). Adherence to layered architecture.
**Scale/Scope**: Single-user console client, supporting a moderate number of in-memory tasks (e.g., up to 1000 tasks for typical usage).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **0) Authority Order**: Acknowledged and followed.
- [x] **1) UV-Only Python Tooling (Hard Rule)**: All Python tooling will exclusively use `uv`.
- [x] **2) Phase I Scope**: Plan strictly adheres to FastAPI backend with in-memory CRUD and console client.
- [x] **3) Architecture Must Be Layered**: The project structure will enforce Domain, Application, Infrastructure, and Interface (API/Console) layers.
- [x] **4) Critical Rule: Controllers Must Be Thin**: API controllers will be minimal, focusing on DTO parsing, use case invocation, and response mapping.
- [x] **5) Extensibility Contract (Phase II–V)**: The design for the InMemoryRepo and use cases will facilitate future swapping to a DBRepo without altering use cases.
- [x] **6) Data Model Must Be Future-Proof**: Task model fields (id, title, description, completed, created_at, updated_at, due_at, priority, tags) are all present.
- [x] **7) ID Generation Rule**: Will implement epoch ms based ID generation with uniqueness suffix.
- [x] **8) Error Handling**: API will return clear messages for not found and validation errors; console will handle gracefully.
- [x] **9) Type Checking + Linting (No Tests)**: `ruff` and `mypy` will be configured and run for linting and type checking. No formal test suite is required, but integration of `ruff` and `mypy` commands will be part of the build process.
- [x] **10) API Stability Rule**: API endpoints will use `/api/v1/` prefix for versioning.

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-api-console/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── domain/              # Task model, validation (no FastAPI)
├── application/         # Use cases (business logic)
├── infrastructure/      # Repository interface, in-memory implementation
├── interfaces/          # API controllers (FastAPI) and Console UI
│   ├── api/             # FastAPI routes
│   └── console/         # Console application
└── main.py              # Application entry point (FastAPI server)

tests/ (placeholder - for ruff/mypy configuration, no functional tests)
├── unit/
├── integration/
└── contract/

# Configuration files
├── pyproject.toml       # uv configuration, ruff, mypy
├── Dockerfile           # For deployment (future)
├── README.md
```

**Structure Decision**: A single project structure is chosen, with a `src/` directory segmented by architectural layers (domain, application, infrastructure, interfaces) to maintain clear separation of concerns and facilitate extensibility as per the constitution. The `interfaces/` layer is further split into `api/` for FastAPI and `console/` for the interactive client. A `main.py` will serve as the entry point for the FastAPI application.

## Complexity Tracking

<!-- No constitution violations to justify. -->

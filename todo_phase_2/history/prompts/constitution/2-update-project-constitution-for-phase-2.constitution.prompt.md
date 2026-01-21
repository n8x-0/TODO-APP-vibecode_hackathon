---
id: 2
title: Update Project Constitution For Phase 2
stage: constitution
date: 2026-01-05
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "phase2", "fastapi", "auth", "cookies", "neon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
This is the Qwen Code. We are setting up the context for our chat.
Today's date is Monday, January 5, 2026 (formatted according to the user's locale).
My operating system is: win32
I'm currently working in the directory: E:\n8x\HACKATHON\hackathon\todo_app\phase_2
Here is the folder structure of the current working directories:

Showing up to 20 items (files + folders). Folders or files indicated with ... contain more items not shown, were ignored, or the display limit (20 items) was reached.

E:\n8x\HACKATHON\hackathon\todo_app\phase_2\
├───.gitignore
├───GEMINI.md
├───pyproject.toml
├───QWEN.md
├───uv.lock
├───.gemini\
│   └───commands\
├───.qwen\
│   └───commands\
├───.specify\
│   ├───memory\
│   ├───scripts\
│   └───templates\
├───.venv\
│   ├───Lib\...
│   └───Scripts\...
├───history\
├───specs\
├───src\
└───tests\

---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: sp.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

/sp.constitution we are moving on to the phase_2, # Speckit Constitution — Phase 2 (FastAPI Auth + Cookies + Neon)

## 1) UV-only backend
All python deps + commands must use uv.
Commit uv.lock. No pip/poetry/pdm.

## 2) Reuse Phase 1 core
Business logic remains in:
- domain/
- app/use_cases.py
- infra/repo.py
Routes stay thin.

## 3) Cookie-based auth is mandatory (backend-issued)
- FastAPI authenticates users and issues auth session/JWT.
- FastAPI sets auth cookie via `Set-Cookie`.
- Cookie must be HttpOnly (and Secure in production).
- Frontend must NOT store tokens in localStorage/sessionStorage.

## 4) User isolation
- `user_id` is derived only from verified cookie/session.
- `user_id` must never be accepted from client request payloads.

## 5) Persistence via Neon Postgres
Replace in-memory repo with Postgres repo only.
No business logic duplication.

## 6) API versioning
All endpoints under /api/v1.

## 7) Type checking + linting
No tests required.
Provide:
- uv run ruff check .
- uv run mypy src
```

## Response snapshot

I've successfully updated the project constitution for Phase 2. Here's the final summary:

## Summary

- **New Version**: 1.0.0 (initial version for Phase 2)
- **Bump Rationale**: This is the initial constitution for Phase 2 of the Speckit Todo App, implementing FastAPI Auth with Cookies and Neon Postgres. The version is set to 1.0.0 as it establishes the foundational principles for this phase.
- **Files Updated**: Only the constitution file at `.specify/memory/constitution.md` was updated.
- **No Manual Follow-up Required**: All dependent templates were checked and found to be compatible with the new constitution without requiring changes.
- **Suggested Commit Message**: `docs: add constitution for Phase 2 (FastAPI Auth + Cookies + Neon)`

The updated constitution now reflects the specific requirements for Phase 2:
1. UV-only backend with all Python dependencies using uv
2. Reuse of Phase 1 core business logic
3. Mandatory cookie-based authentication
4. User isolation with user_id derived only from verified sessions
5. Persistence via Neon Postgres
6. API versioning under /api/v1
7. Type checking and linting requirements

## Outcome

- ✅ Impact: Created new constitution for Phase 2 with 7 core principles
- 🧪 Tests: No tests required for constitution update
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Ready to proceed with feature specification based on updated constitution
- 🧠 Reflection: Constitution properly reflects Phase 2 requirements for FastAPI Auth + Cookies + Neon

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with feature specification based on updated constitution

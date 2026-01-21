---
description: "Task list for Phase I (API-First In-Memory Todo) feature."
---

# Tasks: Todo API Console

**Input**: Design documents from `specs/1-todo-api-console/`
**Prerequisites**: `plan.md` (inferred from constitution/spec), `spec.md` (required), `data-model.md` (inferred from spec), `contracts/` (inferred from spec)

**Tests**: Tests are not explicitly requested in the spec but are included as examples for good practice, marked as optional.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [TaskID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Backend: `backend/src/`, `backend/tests/`
- Console Client: `client/`
- Project root: `pyproject.toml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure (`src/domain/`, `src/application/`, `src/infrastructure/`, `src/interfaces/api/`, `src/interfaces/console/`, `src/main.py`, `tests/`, `pyproject.toml`, `.gitignore`)
- [X] T002 Initialize Python project with `uv` (`pyproject.toml`)
- [X] T003 Configure linting (`ruff`) and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Implement domain `Task` model and initial validation in `src/domain/models/task.py`
- [X] T005 Define repository interface `src/domain/interfaces/task_repository.py`
- [X] T006 Implement in-memory repository `src/infrastructure/repositories/in_memory_task_repository.py`
- [X] T007 Implement base task use cases in `src/application/use_cases/task_use_cases.py`
- [X] T008 Setup FastAPI app and API versioning (`/api/v1/`) in `src/main.py`
- [X] T009 Implement API health check endpoint `src/interfaces/api/health.py`
- [X] T010 Setup console client structure and base API client `src/interfaces/console/cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Start Application & Health Check (Priority: P1) 🎯 MVP

**Goal**: The console application starts, checks backend health, displays the main menu, and handles backend unavailability.

**Independent Test**: Launch the console. Verify menu appears if backend is up, or error and exit if down.

### Implementation for User Story 1

- [X] T011 [P] [US1] Integrate health check call in console API client `src/interfaces/console/api_client.py`
- [X] T012 [US1] Implement health check logic and response handling in console main `src/interfaces/console/cli.py`
- [X] T013 [US1] Implement main menu loop and display in console `src/interfaces/console/cli.py`
- [X] T014 [US1] Add graceful exit logic if backend is unreachable in `src/interfaces/console/cli.py`

**Checkpoint**: User Story 1 complete. Console starts, checks health, shows menu, handles errors.

---

## Phase 4: User Story 2 - Add a New Task (Priority: P1)

**Goal**: Users can add a new todo task via console prompts, which are then sent to the backend API.

**Independent Test**: Add a task and verify it appears in the list.

### Implementation for User Story 2

- [X] T015 [P] [US2] Refine `Task` model validation based on spec in `src/domain/models/task.py`
- [X] T016 [P] [US2] Implement `create_task` use case in `src/application/use_cases/task_use_cases.py`
- [X] T017 [P] [US2] Implement `POST /api/v1/tasks` endpoint and controller logic in `src/interfaces/api/tasks.py`
- [X] T018 [US2] Implement add task CLI interaction and API call in `src/interfaces/console/cli.py`, `src/interfaces/console/task_cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: User Story 2 complete. Task creation functional.

---

## Phase 5: User Story 3 - View/List Tasks (Priority: P1)

**Goal**: Users can view tasks filtered by all, completed, or incomplete status via the console.

**Independent Test**: List tasks after adding them.

### Implementation for User Story 3

- [X] T019 [P] [US3] Implement `list_tasks` use case in `src/application/use_cases/task_use_cases.py`
- [X] T020 [P] [US3] Implement `GET /api/v1/tasks` endpoint in `src/interfaces/api/tasks.py`
- [X] T021 [US3] Implement list tasks CLI interaction and API call in `src/interfaces/console/cli.py`, `src/interfaces/console/task_cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: User Story 3 complete. Task listing and filtering functional.

---

## Phase 6: User Story 4 - Update an Existing Task (Priority: P2)

**Goal**: Users can modify task fields via the console, interacting with the backend API.

**Independent Test**: Update a task and verify changes when listing.

### Implementation for User Story 4

- [X] T022 [P] [US4] Implement `update_task` use case in `src/application/use_cases/task_use_cases.py`
- [X] T023 [P] [US4] Implement `PATCH /api/v1/tasks/{id}` endpoint in `src/interfaces/api/tasks.py`
- [X] T024 [US4] Implement update task CLI interaction and API call in `src/interfaces/console/cli.py`, `src/interfaces/console/task_cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: User Story 4 complete. Task updates functional.

---

## Phase 7: User Story 5 - Toggle Task Completion Status (Priority: P2)

**Goal**: Users can mark a task as complete or incomplete via the console.

**Independent Test**: Toggle a task and observe its new completion status when listing.

### Implementation for User Story 5

- [X] T025 [P] [US5] Implement `toggle_task_completion` use case in `src/application/use_cases/task_use_cases.py`
- [X] T026 [P] [US5] Implement `POST /api/v1/tasks/{id}/toggle` endpoint in `src/interfaces/api/tasks.py`
- [X] T027 [US5] Implement toggle task CLI interaction and API call in `src/interfaces/console/cli.py`, `src/interfaces/console/task_cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: User Story 5 complete. Task completion toggle functional.

---

## Phase 8: User Story 6 - Delete a Task (Priority: P3)

**Goal**: Users can delete tasks via the console after confirmation.

**Independent Test**: Delete a task and verify it no longer appears in the list.

### Implementation for User Story 6

- [X] T028 [P] [US6] Implement `delete_task` use case in `src/application/use_cases/task_use_cases.py`
- [X] T029 [P] [US6] Implement `DELETE /api/v1/tasks/{id}` endpoint in `src/interfaces/api/tasks.py`
- [X] T030 [US6] Implement delete task CLI interaction and API call in `src/interfaces/console/cli.py`, `src/interfaces/console/task_cli.py`, `src/interfaces/console/api_client.py`

**Checkpoint**: User Story 6 complete. Task deletion functional.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T031 Documentation updates
- [X] T032 Code cleanup and refactoring
- [X] T033 Final review and adherence to constitution

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1-US5 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tasks within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tasks for User Story 2 together:
Task: "Refine Task model validation in src/domain/models/task.py"
Task: "Implement create_task use case in src/application/use_cases/task_use_cases.py"
Task: "Implement POST /api/v1/tasks endpoint in src/interfaces/api/tasks.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
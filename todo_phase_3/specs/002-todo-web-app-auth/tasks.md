# Tasks: Todo Web App with Authentication

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create backend directory structure: backend/src/domain/, backend/src/app/, backend/src/infra/, backend/src/auth/, backend/src/api/
- [X] T002 [P] Create frontend directory structure: frontend/src/components/, frontend/src/pages/, frontend/src/services/
- [X] T003 [P] Initialize backend with uv: cd backend && uv init && uv venv
- [X] T004 [P] Add backend dependencies with uv: fastapi, uvicorn, sqlalchemy, asyncpg, alembic, pydantic, ruff, mypy, passlib[bcrypt], python-jose, python-multipart
- [X] T005 Create backend/src/app/main.py with basic FastAPI app
- [X] T006 Create frontend with Next.js 14: npx create-next-app frontend --js --tailwind --eslint --app

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Setup Alembic for database migrations in backend/
- [X] T008 [P] Create database models for User and Task in backend/src/domain/models/
- [X] T009 [P] Create database tables: users, tasks (with indexes) in backend/src/infra/
- [X] T010 [P] Implement password hashing utilities in backend/src/auth/utils.py
- [X] T011 [P] Create JWT encoding/decoding utilities in backend/src/auth/jwt.py
- [X] T012 [P] Create database session management in backend/src/infra/database.py
- [X] T013 [P] Create base repository interface in backend/src/infra/repo.py (from Phase 1)
- [X] T014 [P] Create InMemoryRepo for initial development in backend/src/infra/repo.py (from Phase 1)
- [X] T015 [P] Create Postgres repository implementation in backend/src/infra/postgres_repo.py
- [X] T016 [P] Create get_current_user dependency in backend/src/api/deps.py
- [X] T017 [P] Create auth routes in backend/src/api/routes_auth.py
- [X] T018 [P] Create tasks routes in backend/src/api/routes_tasks.py
- [X] T019 [P] Create environment configuration in backend/src/config.py
- [X] T020 [P] Create error handling middleware in backend/src/middleware/error_handler.py
- [X] T021 [P] Create API v1 router in backend/src/api/v1.py
- [X] T022 [P] Integrate all API routes with main FastAPI app in backend/src/app/main.py
- [X] T023 [P] Create frontend API service for auth in frontend/src/services/auth.js
- [X] T024 [P] Create frontend API service for tasks in frontend/src/services/tasks.js
- [X] T025 [P] Create frontend components: LoginForm, SignupForm, TaskList, TaskForm in frontend/src/components/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts and log in to access the todo application

**Independent Test**: The registration and login flow can be tested independently by creating a new account, logging in, and verifying that the user can access the application.

### Implementation for User Story 1

- [X] T026 [P] [US1] Implement signup endpoint POST /api/v1/auth/signup in backend/src/api/routes_auth.py
- [X] T027 [P] [US1] Implement login endpoint POST /api/v1/auth/login in backend/src/api/routes_auth.py
- [X] T028 [P] [US1] Implement logout endpoint POST /api/v1/auth/logout in backend/src/api/routes_auth.py
- [X] T029 [P] [US1] Implement me endpoint GET /api/v1/auth/me in backend/src/api/routes_auth.py
- [X] T030 [P] [US1] Create signup form component in frontend/src/components/SignupForm.js
- [X] T031 [P] [US1] Create login form component in frontend/src/components/LoginForm.js
- [X] T032 [P] [US1] Create login page in frontend/src/app/login/page.js
- [X] T033 [P] [US1] Create signup page in frontend/src/app/signup/page.js
- [X] T034 [US1] Implement cookie handling in frontend auth service to store session
- [X] T035 [US1] Implement cookie handling in frontend to include credentials in API requests
- [X] T036 [US1] Add cookie security settings: HttpOnly, Secure, SameSite in auth endpoints
- [X] T037 [US1] Add validation for signup/login forms in frontend components
- [X] T038 [US1] Add error handling for auth operations in frontend
- [X] T039 [US1] Redirect to tasks page after successful login/signup in frontend
- [X] T040 [US1] Create basic layout for authenticated vs unauthenticated users in frontend

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: Allow authenticated users to manage their tasks by adding, viewing, updating, and deleting them

**Independent Test**: A user can create tasks, view them in a list, update their status, and delete them independently of other features.

### Implementation for User Story 2

- [X] T041 [P] [US2] Implement GET /api/v1/tasks endpoint in backend/src/api/routes_tasks.py
- [X] T042 [P] [US2] Implement POST /api/v1/tasks endpoint in backend/src/api/routes_tasks.py
- [X] T043 [P] [US2] Implement PATCH /api/v1/tasks/{id} endpoint in backend/src/api/routes_tasks.py
- [X] T044 [P] [US2] Implement POST /api/v1/tasks/{id}/toggle endpoint in backend/src/api/routes_tasks.py
- [X] T045 [P] [US2] Implement DELETE /api/v1/tasks/{id} endpoint in backend/src/api/routes_tasks.py
- [X] T046 [P] [US2] Create TaskList component in frontend/src/components/TaskList.js
- [X] T047 [P] [US2] Create TaskItem component in frontend/src/components/TaskItem.js
- [X] T048 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.js
- [X] T049 [P] [US2] Create tasks page in frontend/src/app/tasks/page.js
- [X] T050 [US2] Add filtering functionality (all/completed/incomplete) to TaskList component
- [X] T051 [US2] Implement task creation functionality in frontend
- [X] T052 [US2] Implement task update functionality in frontend
- [X] T053 [US2] Implement task toggle functionality in frontend
- [X] T054 [US2] Implement task deletion functionality with confirmation in frontend
- [X] T055 [US2] Add loading and error states to task operations in frontend
- [X] T056 [US2] Add empty state for task list in frontend
- [X] T057 [US2] Add responsive design to task management UI in frontend

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Session Persistence (Priority: P2)

**Goal**: Ensure authenticated users remain logged in across browser sessions

**Independent Test**: A user can close and reopen the browser and remain logged in until the session expires.

### Implementation for User Story 3

- [X] T058 [P] [US3] Configure session cookie expiration in auth endpoints
- [X] T059 [P] [US3] Implement session refresh mechanism in backend
- [X] T060 [P] [US3] Add session validation middleware to protected endpoints
- [X] T061 [US3] Implement automatic session refresh in frontend when making API calls
- [X] T062 [US3] Handle 401 responses by redirecting to login in frontend
- [X] T063 [US3] Add session persistence across browser restarts in frontend
- [X] T064 [US3] Add session timeout handling in frontend
- [X] T065 [US3] Create middleware to check authentication status in frontend
- [X] T066 [US3] Add "Remember me" functionality to login in frontend
- [X] T067 [US3] Implement proper session cleanup on logout in backend and frontend

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T068 [P] Add comprehensive input validation to all API endpoints
- [X] T069 [P] Add rate limiting to auth endpoints
- [X] T070 [P] Add comprehensive logging throughout the application
- [X] T071 [P] Add unit tests for backend services
- [X] T072 [P] Add integration tests for API endpoints
- [X] T073 [P] Add UI tests for frontend components
- [X] T074 [P] Add security headers to API responses
- [X] T075 [P] Add environment-specific configurations
- [X] T076 [P] Add documentation for API endpoints
- [X] T077 [P] Add error boundaries in frontend
- [X] T078 [P] Add proper loading states throughout the frontend
- [X] T079 [P] Add proper error handling throughout the frontend
- [X] T080 [P] Add responsive design improvements to frontend
- [X] T081 [P] Add accessibility improvements to frontend
- [X] T082 [P] Add performance optimizations to frontend
- [X] T084 [P] Add proper meta tags and descriptions to frontend
- [X] T085 Run linting: uv run ruff check . in backend
- [X] T086 Run type checking: uv run mypy src in backend
- [X] T087 Run frontend linting: npm run lint in frontend
- [X] T088 Run frontend formatting: npm run format in frontend
- [X] T089 Run quickstart validation: Follow quickstart.md instructions to verify setup works

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

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
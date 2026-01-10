# Feature Specification: Todo Web App with Authentication

**Feature Branch**: `2-todo-web-app-auth`
**Created**: 2026-01-05
**Status**: Draft
**Input**: User description: "# Speckit Specify — Phase 2 (Web + Auth Cookies + DB) ## A) Objective Build a full-stack todo web app: - Backend: FastAPI + Neon Postgres - Frontend: Next.js 14 responsive UI - Auth: backend-issued cookie session/JWT - Features: Add, List, Update, Toggle, Delete ## B) Auth Flow (correct model) 1) Browser submits login/signup to FastAPI 2) FastAPI validates credentials 3) FastAPI sets HttpOnly cookie using Set-Cookie 4) Browser includes cookie automatically in future requests 5) Backend verifies cookie; returns 401 if invalid/missing Acceptance: - Refresh stays logged in (cookie persists). - Missing/invalid cookie → 401. - Tasks are scoped to authenticated user. ## C) Endpoints (v1) ### Auth - POST /api/v1/auth/signup - POST /api/v1/auth/login - POST /api/v1/auth/logout - GET /api/v1/auth/me ### Tasks (protected) - GET /api/v1/tasks?status=all|completed|incomplete - POST /api/v1/tasks - PATCH /api/v1/tasks/{id} - POST /api/v1/tasks/{id}/toggle - DELETE /api/v1/tasks/{id} ## D) Data Model Task: - id (string; Date.now-like OK) - user_id (string, from cookie auth) - title (<=200) - description (string; can be empty) - completed bool - created_at, updated_at - due_at nullable - priority nullable (low|medium|high) - tags json/array Indexes: - user_id - (user_id, completed) ## E) UI Requirements - /login, /signup, /tasks pages - Filters all/completed/incomplete - Delete requires confirmation - Responsive layout + loading/error/empty states"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Login (Priority: P1)

A new user needs to create an account and log in to access the todo application. The user should be able to sign up with their email and password, then log in to access their tasks.

**Why this priority**: This is the foundational user journey that enables all other functionality. Without authentication, users cannot access the todo features.

**Independent Test**: The registration and login flow can be tested independently by creating a new account, logging in, and verifying that the user can access the application.

**Acceptance Scenarios**:

1. **Given** a user is on the signup page, **When** they enter valid credentials and submit, **Then** an account is created and they are logged in
2. **Given** a user has an account, **When** they enter valid credentials on the login page, **Then** they are authenticated and redirected to their tasks page
3. **Given** a user enters invalid credentials, **When** they attempt to log in, **Then** they receive an error message and remain on the login page

---

### User Story 2 - Task Management (Priority: P1)

An authenticated user needs to manage their tasks by adding, viewing, updating, and deleting them. This includes toggling task completion status and filtering tasks.

**Why this priority**: This is the core functionality of the todo application that users will use most frequently.

**Independent Test**: A user can create tasks, view them in a list, update their status, and delete them independently of other features.

**Acceptance Scenarios**:

1. **Given** an authenticated user is on the tasks page, **When** they add a new task, **Then** the task appears in their task list
2. **Given** a user has tasks, **When** they toggle a task's completion status, **Then** the task status updates in the list
3. **Given** a user has multiple tasks, **When** they apply filters (all/completed/incomplete), **Then** the task list updates to show only matching tasks
4. **Given** a user wants to delete a task, **When** they confirm deletion, **Then** the task is removed from their list

---

### User Story 3 - Session Persistence (Priority: P2)

An authenticated user should remain logged in across browser sessions until they explicitly log out or their session expires.

**Why this priority**: This enhances user experience by eliminating the need to log in repeatedly.

**Independent Test**: A user can close and reopen the browser and remain logged in until the session expires.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they refresh the page, **Then** they remain authenticated
2. **Given** a user is logged in, **When** they close and reopen the browser, **Then** they remain authenticated
3. **Given** a user's session has expired or they have invalid credentials, **When** they make a request, **Then** they receive a 401 error and are redirected to login

---

### Edge Cases

- What happens when a user tries to access a task that doesn't belong to them?
- How does the system handle concurrent sessions from multiple browsers/devices?
- What happens when a user's session expires while they're actively using the application?
- How does the system handle malformed or tampered authentication cookies?
- What happens when a user attempts to create a task with invalid data?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create accounts via signup endpoint
- **FR-002**: System MUST authenticate users via login endpoint
- **FR-003**: System MUST issue HttpOnly cookies upon successful authentication
- **FR-004**: System MUST validate authentication cookies for protected endpoints
- **FR-005**: System MUST return 401 error for requests with missing or invalid authentication
- **FR-006**: System MUST allow authenticated users to create new tasks
- **FR-007**: System MUST allow authenticated users to view their tasks with filtering options
- **FR-008**: System MUST allow authenticated users to update task details
- **FR-009**: System MUST allow authenticated users to toggle task completion status
- **FR-010**: System MUST allow authenticated users to delete tasks
- **FR-011**: System MUST scope tasks to authenticated user (user can only access their own tasks)
- **FR-012**: System MUST provide a logout endpoint that invalidates the session
- **FR-013**: System MUST provide an endpoint to retrieve current user information

### Key Entities *(include if feature involves data)*

- **User**: Represents a registered user with authentication credentials
- **Task**: Represents a todo item with title, description, completion status, timestamps, due date, priority, and tags

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 1 minute
- **SC-002**: Users can log in and access their tasks in under 10 seconds
- **SC-003**: 95% of authenticated users can successfully create, view, update, and delete tasks
- **SC-004**: Session cookies persist across browser restarts for at least 7 days
- **SC-005**: 99% of requests with valid authentication succeed, while 99% of requests with invalid authentication return 401
- **SC-006**: Task filtering operations return results in under 2 seconds
- **SC-007**: Users can complete task deletion with confirmation in under 5 seconds

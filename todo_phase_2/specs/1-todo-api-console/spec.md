# Feature Specification: Todo API Console

**Feature Branch**: `N/A`  
**Created**: 2025-12-27  
**Status**: Draft  
**Input**: User description: "read specs.txt file and create specification accordingly"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start Application & Health Check (Priority: P1)

The console application starts, checks if the backend API is reachable, and then displays the main menu, looping for user input. If the backend is not reachable, it informs the user and exits.

**Why this priority**: Essential for the application to function.

**Independent Test**: Launch the console. Verify menu appears if backend is up, or error and exit if down.

**Acceptance Scenarios**:

1.  **Given** the console app starts and the backend API is running, **When** the console initializes, **Then** it shows the main menu and prompts for input.
2.  **Given** the console app starts and the backend API is unreachable, **When** the console initializes, **Then** it prints an error message and exits gracefully.

---

### User Story 2 - Add a New Task (Priority: P1)

Users can add a new todo task by providing a title, optional description, due date, priority, and tags through the console, which then calls the backend API.

**Why this priority**: Core functionality for a todo app.

**Independent Test**: Can be tested by adding a task and then verifying it appears in the list.

**Acceptance Scenarios**:

1.  **Given** the console is at the main menu, **When** the user chooses to add a task and provides valid details, **Then** the task is created via the API, and its ID is displayed.
2.  **Given** the console is at the main menu, **When** the user chooses to add a task and provides invalid details (e.g., missing title), **Then** validation errors are shown, and the user returns to the menu.

---

### User Story 3 - View/List Tasks (Priority: P1)

Users can view a list of all, completed, or incomplete tasks from the console, which fetches data from the backend API.

**Why this priority**: Core functionality to see existing tasks.

**Independent Test**: Can be tested by listing tasks after adding them.

**Acceptance Scenarios**:

1.  **Given** there are tasks in the system, **When** the user chooses to list tasks (all/completed/incomplete), **Then** the console displays tasks with their ID, title, and completion status.
2.  **Given** there are no tasks in the system, **When** the user chooses to list tasks, **Then** the console prints "No tasks found."

---

### User Story 4 - Update an Existing Task (Priority: P2)

Users can modify specific fields of an existing task (title, description, due date, priority, tags) by providing the task ID and new values via the console, interacting with the backend API.

**Why this priority**: Important for managing tasks, but viewing and adding are more critical initially.

**Independent Test**: Update a task and verify changes when listing.

**Acceptance Scenarios**:

1.  **Given** an existing task, **When** the user provides a valid task ID and new field values, **Then** the task is updated, and the updated fields are shown.
2.  **Given** a non-existent task ID, **When** the user attempts to update a task, **Then** a "not found" message is displayed, and the user returns to the menu.
3.  **Given** an existing task, **When** the user provides invalid field values for an update, **Then** validation errors are shown, and the user returns to the menu.

---

### User Story 5 - Toggle Task Completion Status (Priority: P2)

Users can mark a task as complete or incomplete by providing its ID through the console, which triggers the toggle endpoint on the backend API.

**Why this priority**: Key task management action.

**Independent Test**: Toggle a task and observe its new completion status when listing.

**Acceptance Scenarios**:

1.  **Given** an existing task, **When** the user provides a valid task ID to toggle, **Then** the task's completion status is flipped, and the new status is printed.
2.  **Given** a non-existent task ID, **When** the user attempts to toggle a task, **Then** a "not found" message is displayed, and the user returns to the menu.

---

### User Story 6 - Delete a Task (Priority: P3)

Users can delete an existing task by providing its ID and confirming the deletion via the console, which calls the backend API.

**Why this priority**: Destructive action, less frequent than other CRUD operations.

**Independent Test**: Delete a task and verify it no longer appears in the list.

**Acceptance Scenarios**:

1.  **Given** an existing task, **When** the user provides a valid task ID and confirms deletion, **Then** the task is removed from the system.
2.  **Given** an existing task, **When** the user provides a valid task ID but cancels deletion, **Then** the task remains in the system.
3.  **Given** a non-existent task ID, **When** the user attempts to delete a task, **Then** a "not found" message is displayed, and the user returns to the menu.

---

### Edge Cases

-   What happens when a user input for a task field (e.g., `due_at`) is in an invalid format?
-   How does the system handle concurrent updates to the same task (though in-memory is simple, this is a general question)?
-   What if the backend API experiences an internal server error during an operation?

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide a FastAPI backend for Todo CRUD operations.
-   **FR-002**: The console application MUST provide an interactive menu for users to interact with Todo tasks.
-   **FR-003**: The console MUST perform a health check against the backend API upon startup.
-   **FR-004**: The console MUST allow users to add new tasks with a title (required), description, due date, priority, and tags (all optional except title).
-   **FR-005**: The console MUST allow users to view tasks, filtering by all, completed, or incomplete status.
-   **FR-006**: The console MUST allow users to update existing tasks by ID, modifying any of their fields.
-   **FR-007**: The console MUST allow users to toggle the completion status of a task by ID.
-   **FR-008**: The console MUST allow users to delete tasks by ID, requiring confirmation.
-   **FR-009**: The backend API MUST expose the following endpoints:
    *   `GET /api/v1/health`
    *   `POST /api/v1/tasks`
    *   `GET /api/v1/tasks?status=...`
    *   `GET /api/v1/tasks/{id}` (optional for console, but specified for API)
    *   `PATCH /api/v1/tasks/{id}`
    *   `POST /api/v1/tasks/{id}/toggle`
    *   `DELETE /api/v1/tasks/{id}`
-   **FR-010**: The API MUST return appropriate HTTP status codes (200, 201, 400, 404) for its operations.
-   **FR-011**: The API MUST validate incoming task data (title required and length, due_at format, priority values, tags normalization).

### Key Entities *(include if feature involves data)*

-   **Task**: Represents a single todo item.
    *   Attributes: `id` (string), `title` (string), `description` (string), `completed` (boolean), `created_at` (UTC ISO string), `updated_at` (UTC ISO string), `due_at` (UTC ISO string | null), `priority` (low|medium|high | null), `tags` (list of strings).

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: Users can successfully start the console application and see the main menu within 5 seconds, provided the backend is reachable.
-   **SC-002**: Users can create, view, update, toggle, and delete tasks via the console, with each operation completing within 2 seconds.
-   **SC-003**: The console application gracefully handles an unreachable backend, informing the user and exiting without error.
-   **SC-004**: All API endpoints defined in the API contract respond correctly to valid and invalid requests.
-   **SC-005**: Data validation rules for task fields are enforced by the API, providing clear error messages for invalid input.

## Clarifications

### Session 2025-12-27

- Q: How should the system handle different user types or permissions, even in a single-user context? → A: No distinct roles. The system is designed for a single, implicit user. No permission checks needed for Phase I.

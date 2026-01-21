# Data Model: Task Entity

**Date**: 2025-12-27

## Entity: Task

Represents a single todo item within the system.

### Attributes

-   `id`: `string`
    *   **Description**: Unique identifier for the task.
    *   **Validation**: Generated using epoch milliseconds with uniqueness suffix (as per Constitution).
-   `title`: `string`
    *   **Description**: The main title or subject of the todo task.
    *   **Validation**: Required, maximum length 200 characters.
-   `description`: `string`
    *   **Description**: Optional, detailed description of the task.
    *   **Validation**: Optional, can be empty.
-   `completed`: `boolean`
    *   **Description**: Indicates whether the task has been completed.
    *   **Validation**: Defaults to `false` (implicit, but common practice), can be toggled.
-   `created_at`: `string`
    *   **Description**: Timestamp when the task was created (UTC ISO format).
    *   **Validation**: Automatically set by the system upon creation.
-   `updated_at`: `string`
    *   **Description**: Timestamp when the task was last updated (UTC ISO format).
    *   **Validation**: Automatically updated by the system on modification.
-   `due_at`: `string | null`
    *   **Description**: Optional due date for the task (UTC ISO format).
    *   **Validation**: Must be a valid ISO datetime string if provided, otherwise `null`.
-   `priority`: `string | null`
    *   **Description**: Optional priority level for the task.
    *   **Validation**: Must be one of `"low"`, `"medium"`, `"high"` if provided, otherwise `null`.
-   `tags`: `array<string>`
    *   **Description**: Optional list of tags associated with the task for categorization.
    *   **Validation**: Normalized (trimmed, empty tags removed, duplicates removed) if provided, otherwise empty array or `null`.

### Relationships

-   No explicit relationships with other entities in Phase I.

### State Transitions

-   A task's `completed` status can transition between `true` and `false` via the toggle operation.
-   Other attributes can be updated via the patch operation.

# Tasks API Contract

## GET /api/v1/tasks

### Description
Retrieves a list of tasks for the authenticated user.

### Query Parameters
- status (optional): Filter by status - "all", "completed", "incomplete" (default: "all")

### Response (200 OK)
```json
{
  "tasks": [
    {
      "id": "task-uuid",
      "user_id": "user-uuid",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "due_at": "2023-01-10T00:00:00Z",
      "priority": "medium",
      "tags": ["work", "important"]
    }
  ]
}
```

### Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

### Headers
- Requires authentication cookie
- Content-Type: application/json

---

## POST /api/v1/tasks

### Description
Creates a new task for the authenticated user.

### Request
```json
{
  "title": "New task",
  "description": "Task description",
  "due_at": "2023-01-10T00:00:00Z",
  "priority": "medium",
  "tags": ["work", "important"]
}
```

### Response (201 Created)
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "due_at": "2023-01-10T00:00:00Z",
  "priority": "medium",
  "tags": ["work", "important"]
}
```

### Response (400 Bad Request)
```json
{
  "detail": "Error message explaining why the request failed"
}
```

### Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

### Headers
- Requires authentication cookie
- Content-Type: application/json

---

## PATCH /api/v1/tasks/{id}

### Description
Updates an existing task for the authenticated user.

### Request
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "due_at": "2023-01-15T00:00:00Z",
  "priority": "high",
  "tags": ["work", "urgent"]
}
```

### Response (200 OK)
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Updated task title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "due_at": "2023-01-15T00:00:00Z",
  "priority": "high",
  "tags": ["work", "urgent"]
}
```

### Response (400 Bad Request)
```json
{
  "detail": "Error message explaining why the request failed"
}
```

### Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

### Response (404 Not Found)
```json
{
  "detail": "Task not found"
}
```

### Headers
- Requires authentication cookie
- Content-Type: application/json

---

## POST /api/v1/tasks/{id}/toggle

### Description
Toggles the completion status of a task for the authenticated user.

### Response (200 OK)
```json
{
  "id": "task-uuid",
  "user_id": "user-uuid",
  "title": "Task title",
  "description": "Task description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "due_at": "2023-01-10T00:00:00Z",
  "priority": "medium",
  "tags": ["work", "important"]
}
```

### Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

### Response (404 Not Found)
```json
{
  "detail": "Task not found"
}
```

### Headers
- Requires authentication cookie
- Content-Type: application/json

---

## DELETE /api/v1/tasks/{id}

### Description
Deletes a task for the authenticated user.

### Response (200 OK)
```json
{
  "message": "Task deleted successfully"
}
```

### Response (401 Unauthorized)
```json
{
  "detail": "Not authenticated"
}
```

### Response (404 Not Found)
```json
{
  "detail": "Task not found"
}
```

### Headers
- Requires authentication cookie
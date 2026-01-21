# Data Model: Todo Web App with Authentication

## Entities

### User
Represents a registered user in the system.

**Fields:**
- id (string): Unique identifier for the user
- email (string): User's email address (unique, required)
- hashed_password (string): Bcrypt hashed password (required)
- created_at (datetime): Timestamp when the user was created
- updated_at (datetime): Timestamp when the user was last updated
- is_active (bool): Whether the user account is active

**Validation:**
- Email must be a valid email format
- Email must be unique
- Password must meet minimum security requirements (e.g., minimum length)

### Task
Represents a todo item in the system.

**Fields:**
- id (string): Unique identifier for the task (Date.now-like OK as specified)
- user_id (string): Foreign key referencing the user who owns the task (required)
- title (string): Task title (max 200 characters, required)
- description (string): Optional task description
- completed (bool): Whether the task is completed (default: false)
- created_at (datetime): Timestamp when the task was created
- updated_at (datetime): Timestamp when the task was last updated
- due_at (datetime, nullable): Optional due date for the task
- priority (string, nullable): Task priority (low|medium|high, default: medium)
- tags (json/array): Optional array of tags for the task

**Validation:**
- Title must be between 1 and 200 characters
- User_id must reference a valid user
- Priority must be one of 'low', 'medium', or 'high'
- Due_at must be a valid future date if provided

### Session (Optional - if using opaque sessions)
Represents an active user session.

**Fields:**
- id (string): Unique session identifier
- user_id (string): Foreign key referencing the user (required)
- session_token (string): Unique token for the session (required)
- expires_at (datetime): When the session expires
- created_at (datetime): Timestamp when the session was created
- is_active (bool): Whether the session is still valid

## Relationships

- User (1) → Task (Many): A user can have many tasks
- User (1) → Session (Many): A user can have multiple active sessions (optional)

## Indexes

- User: email (unique)
- Task: user_id (for efficient user task queries)
- Task: (user_id, completed) (for efficient filtering by user and completion status)
- Task: due_at (for efficient sorting by due date)
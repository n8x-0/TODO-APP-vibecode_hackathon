# Auth API Contract

## POST /api/v1/auth/signup

### Description
Creates a new user account.

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Response (200 OK)
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Response (400 Bad Request)
```json
{
  "detail": "Error message explaining why the request failed"
}
```

### Response (409 Conflict)
```json
{
  "detail": "Email already registered"
}
```

### Headers
- Sets HttpOnly cookie with session token
- Content-Type: application/json

---

## POST /api/v1/auth/login

### Description
Authenticates a user and returns session information.

### Request
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

### Response (200 OK)
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z"
}
```

### Response (400 Bad Request)
```json
{
  "detail": "Invalid email or password"
}
```

### Headers
- Sets HttpOnly cookie with session token
- Content-Type: application/json

---

## POST /api/v1/auth/logout

### Description
Logs out the current user and invalidates the session.

### Response (200 OK)
```json
{
  "message": "Successfully logged out"
}
```

### Headers
- Clears the authentication cookie

---

## GET /api/v1/auth/me

### Description
Returns information about the currently authenticated user.

### Response (200 OK)
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
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
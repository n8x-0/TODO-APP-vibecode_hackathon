<!--
Sync Impact Report:
Version change: 1.0.0 → 2.0.0 (major update for Phase 3)
List of modified principles:
- Added "MCP Server Architecture": All AI interactions must go through MCP server exposing standardized tools for task operations.
- Added "Stateless AI Server": Chat endpoint maintains no in-memory state; all conversation state stored in database.
- Added "OpenAI Agents SDK Integration": Use OpenAI Agents SDK for AI logic and conversation management.
- Added "SQLModel ORM Standard": Use SQLModel for all database operations across all services.
- Added "Claude Code Integration": All implementation must follow Claude Code and Spec-Kit Plus methodology.
Modified principles:
- Modified "API Versioning" to include MCP endpoints under /mcp/v1.
Removed sections: None
Added sections:
- "MCP Tool Specifications" section: Defines standardized interfaces for task operations.
- "AI Conversation Flow" section: Outlines stateless request cycle for chat interactions.
- "Database Schema Requirements" section: Specifies models for tasks, conversations, and messages.
Templates requiring updates:
- ✅ plan-template.md - Updated to include MCP and AI considerations
- ✅ spec-template.md - Updated to include MCP and AI requirements
- ✅ tasks-template.md - Updated to include MCP and AI task categories
- ✅ All templates checked, no specific updates required
Follow-up TODOs: None
-->
# Speckit Todo App - Phase 3 (MCP Server + AI Chatbot) Constitution

## Core Principles

### MCP Server Architecture
All AI interactions must go through MCP server exposing standardized tools for task operations. The MCP server must use the official MCP SDK and expose tools for add_task, list_tasks, complete_task, delete_task, and update_task operations.

### Stateless AI Server
Chat endpoint maintains no in-memory state; all conversation state stored in database. Server must be ready for any request without holding state between calls, enabling horizontal scalability.

### OpenAI Agents SDK Integration
Use OpenAI Agents SDK for AI logic and conversation management. The AI agent must use MCP tools to perform all task operations rather than direct API calls.

### SQLModel ORM Standard
Use SQLModel for all database operations across all services (backend, MCP server). Maintain consistent data models across services.

### Claude Code Integration
All implementation must follow Claude Code and Spec-Kit Plus methodology. Write spec → Generate plan → Break into tasks → Implement via Claude Code.

### Cookie-Based Authentication
FastAPI authenticates users and issues auth session/JWT. FastAPI sets auth cookie via Set-Cookie. Cookie must be HttpOnly (and Secure in production). Frontend must NOT store tokens in localStorage/sessionStorage.

### User Isolation
user_id is derived only from verified cookie/session. user_id must never be accepted from client request payloads.

### Neon Postgres Persistence
Replace in-memory repo with Postgres repo only. No business logic duplication. All services must use the same database schema.

### API Versioning
All backend endpoints under /api/v1. All MCP endpoints under /mcp/v1.

## MCP Tool Specifications
The MCP server must expose the following standardized tools:
- add_task: Create a new task with title and description
- list_tasks: Retrieve tasks with optional status filter
- complete_task: Mark a task as complete
- delete_task: Remove a task from the list
- update_task: Modify task title or description

## AI Conversation Flow
Each conversation follows a stateless request cycle:
1. Receive user message with conversation_id
2. Fetch conversation history from database
3. Build message array for agent (history + new message)
4. Store user message in database
5. Run agent with MCP tools
6. Agent invokes appropriate MCP tool(s)
7. Store assistant response in database
8. Return response to client

## Database Schema Requirements
Database must include models for:
- Task: user_id, id, title, description, completed, created_at, updated_at
- Conversation: user_id, id, created_at, updated_at
- Message: user_id, id, conversation_id, role (user/assistant), content, created_at

## Type Checking and Linting
No tests required. Provide: uv run ruff check . and uv run mypy src for all services.

## Development Workflow
Follow Spec-Driven Development (SDD) methodology with Prompt History Records (PHRs) for all user interactions and Architectural Decision Records (ADRs) for significant decisions. All implementation must use Claude Code methodology.

## Governance
Constitution supersedes all other practices. Amendments require documentation and migration plan. All PRs/reviews must verify compliance with these principles.

**Version**: 2.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19
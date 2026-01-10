# Quickstart Guide: Todo Web App with Authentication

## Prerequisites

- Python 3.11+
- Node.js 18+
- uv package manager
- PostgreSQL (or access to Neon Postgres)
- Docker (optional, for local development)

## Setup Instructions

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up Python environment**
   ```bash
   # Install uv if you don't have it
   pip install uv
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r backend/requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file in backend directory
   cp backend/.env.example backend/.env
   # Edit backend/.env with your database credentials and other settings
   ```

4. **Set up the database**
   ```bash
   # Run database migrations
   cd backend
   uv run alembic upgrade head
   ```

5. **Run the backend server**
   ```bash
   cd backend
   uv run uvicorn src.app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   ```bash
   # Create .env.local file
   cp .env.example .env.local
   # Edit .env.local with your API endpoint and other settings
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Create a new account
- `POST /api/v1/auth/login` - Log in to an account
- `POST /api/v1/auth/logout` - Log out of the current session
- `GET /api/v1/auth/me` - Get current user information

### Tasks
- `GET /api/v1/tasks` - Get user's tasks
- `POST /api/v1/tasks` - Create a new task
- `PATCH /api/v1/tasks/{id}` - Update a task
- `POST /api/v1/tasks/{id}/toggle` - Toggle task completion
- `DELETE /api/v1/tasks/{id}` - Delete a task

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todo_app
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running Tests

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Linting and Formatting

### Backend
```bash
cd backend
uv run ruff check .
uv run mypy src
```

### Frontend
```bash
cd frontend
npm run lint
npm run format
```

## Deployment

### Backend
1. Ensure all environment variables are set in your deployment environment
2. Run database migrations
3. Start the application server

### Frontend
1. Build the application: `npm run build`
2. Serve the built files using your preferred web server
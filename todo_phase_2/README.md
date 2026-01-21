# Todo Web App with Authentication

This is a full-stack todo web application with authentication using FastAPI backend, Neon Postgres database, and Next.js 14 frontend.

## Quickstart

### Prerequisites

- Python 3.13+
- Node.js 18+
- uv package manager

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. Run the backend server:
   ```bash
   uv run uvicorn src.app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend API URL
   ```

4. Run the frontend development server:
   ```bash
   npm run dev
   ```

### Running the Application

1. Start the backend server (port 8000)
2. Start the frontend server (port 3000)
3. Open your browser to http://localhost:3000

### API Documentation

The API documentation is available at http://localhost:8000/docs when the backend is running.
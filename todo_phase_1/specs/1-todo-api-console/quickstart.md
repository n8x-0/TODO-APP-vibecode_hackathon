# Quickstart Guide: Todo API Console

**Date**: 2025-12-27

This guide provides instructions to set up and run the Todo API backend and its interactive console client.

## Prerequisites

-   Python 3.11+
-   `uv` (Ultrafast Python package installer and resolver) - Install via `curl -LsSf https://astral.sh/uv/install.sh | sh` or equivalent for your OS.

## Setup

1.  **Clone the repository** (if not already cloned):
    ```bash
    git clone <repository-url>
    cd todo_app/phase_1
    ```

2.  **Create a virtual environment and install dependencies** using `uv`:
    ```bash
    uv venv
    uv pip install fastapi uvicorn httpx
    ```
    *Note: `httpx` is suggested for the console client, `uvicorn` for running FastAPI.* 

3.  **Activate the virtual environment**:
    -   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

## Running the Application

### 1. Start the FastAPI Backend

Navigate to the project root and run the FastAPI application. (Assuming `main.py` is the entry point as per the plan's project structure).

```bash
# Ensure virtual environment is activated
uvicorn src.main:app --reload
```

The API will be accessible at `http://localhost:8000/api/v1` (or the port specified by uvicorn).

### 2. Run the Console Client

Open a **new terminal window** (keep the backend running in the first terminal). Navigate to the project root and activate the virtual environment.

```bash
# Ensure virtual environment is activated
python src/interfaces/console/cli.py # Assuming cli.py is the entry point for console
```

The console application will start, attempt to connect to the backend, and present an interactive menu.

## Linting and Type Checking

To ensure code quality, run `ruff` and `mypy`:

```bash
# Ensure virtual environment is activated
uv run ruff check src/
uv run mypy src/
```

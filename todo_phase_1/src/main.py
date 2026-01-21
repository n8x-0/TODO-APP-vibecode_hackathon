"""
Main application entry point for the Todo API.
"""
from fastapi import FastAPI
from interfaces.api.health import router as health_router
from interfaces.api.tasks import router as tasks_router

app = FastAPI(title="Todo API", version="1.0.0")

# Include API routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
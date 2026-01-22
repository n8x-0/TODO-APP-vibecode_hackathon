from fastapi import FastAPI
from src.api.v1 import api_router
from src.middleware.error_handler import add_exception_handlers
import logging
import sys
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager, AsyncExitStack
from dotenv import load_dotenv
from src.infra.database import engine
from src.infra.db_models.models import Base
from src.mcp.server import get_mcp_server
load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize MCP server (Official SDK)
mcp_server = get_mcp_server()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown."""
    async with AsyncExitStack() as stack:
        # Startup
        await stack.enter_async_context(mcp_server.session_manager.run())
        logger.info(f"MCP Server initialized: {mcp_server.name}")
        logger.info("Starting TodoList API...")
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized")

        yield

        # Shutdown
        # Close database connection
        logger.info("Shutting down TodoList Pro API...")
        async with engine.begin() as conn:
            await conn.close()
        logger.info("Database connection closed")

app = FastAPI(
    title="Todo App API",
    redirect_slashes=False,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todo-app-vibecode-hackathon.vercel.app", "http://localhost:3000"],  # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Add exception handlers
add_exception_handlers(app)

# Include API routes
app.include_router(api_router)
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

app.mount("/", app=mcp_server.streamable_http_app())

@app.get("/api/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}
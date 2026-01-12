# from fastapi import FastAPI
# from src.api.v1 import api_router
# from src.middleware.error_handler import add_exception_handlers
# import logging
# import sys
# from starlette.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# from src.infra.database import engine
# from src.infra.db_models.models import Base
# load_dotenv()  # Load environment variables from .env file

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# logger = logging.getLogger(__name__)

# app = FastAPI(title="Todo App API")

# # Create database tables on startup
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Creating database tables...")
#     async with engine.begin() as conn:
#         # Create all tables
#         await conn.run_sync(Base.metadata.create_all)
#     logger.info("Database tables created successfully")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, change this to your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.middleware("http")
# async def add_security_headers(request, call_next):
#     response = await call_next(request)
#     # Add security headers
#     response.headers["X-Content-Type-Options"] = "nosniff"
#     response.headers["X-Frame-Options"] = "DENY"
#     response.headers["X-XSS-Protection"] = "1; mode=block"
#     response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
#     return response

# # Add exception handlers
# add_exception_handlers(app)

# # Include API routes
# app.include_router(api_router)

# @app.get("/")
# def read_root():
#     logger.info("Root endpoint accessed")
#     return {"Hello": "World"}


# @app.get("/api/health")
# def health_check():
#     logger.info("Health check endpoint accessed")
#     return {"status": "healthy"}


# # if __name__ == "__main__":
# #     logger.info("Starting application")
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8000)
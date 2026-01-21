from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


class ErrorHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_with_error_handling(message):
            if message["type"] == "http.response.start":
                # Handle the response start
                pass
            elif message["type"] == "http.response.body":
                # Handle the response body
                pass
            await send(message)

        try:
            await self.app(scope, receive, send_with_error_handling)
        except HTTPException as e:
            # Handle HTTP exceptions
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            await response(scope, receive, send)
        except Exception as e:
            # Handle unexpected exceptions
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
            await response(scope, receive, send)


# Alternative approach using FastAPI's exception handlers
def add_exception_handlers(app):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
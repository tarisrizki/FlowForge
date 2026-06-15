from fastapi import FastAPI
from app.core.config import settings
from app.core.exceptions import CustomException, custom_exception_handler, global_exception_handler

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Register exception handlers
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    # Register routers here
    from app.routers import workflows, webhooks
    app.include_router(workflows.router, prefix="/api/v1")
    app.include_router(webhooks.router, prefix="/api/v1")

    @app.get("/", tags=["Health"])
    async def health_check():
        from app.core.responses import BaseResponse
        return BaseResponse(message="API is running")

    return app

app = create_app()

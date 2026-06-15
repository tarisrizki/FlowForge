from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.responses import BaseResponse

class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(success=False, message=exc.message).model_dump()
    )

async def global_exception_handler(request: Request, exc: Exception):
    # Log the exception here in a real application
    print(f"Global exception caught: {exc}")
    return JSONResponse(
        status_code=500,
        content=BaseResponse(success=False, message="Internal Server Error").model_dump()
    )

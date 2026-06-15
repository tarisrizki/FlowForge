from fastapi import APIRouter, Query
from app.core.responses import BaseResponse
from app.services.example import ExampleService

router = APIRouter(prefix="/example", tags=["Example"])

@router.get("/", response_model=BaseResponse[dict])
async def get_example(fail: bool = Query(False, description="Set to true to trigger an error")):
    data = await ExampleService.get_example_data(fail=fail)
    return BaseResponse(data=data)

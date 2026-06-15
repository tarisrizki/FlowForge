from app.core.exceptions import CustomException

class ExampleService:
    @staticmethod
    async def get_example_data(fail: bool = False) -> dict:
        if fail:
            raise CustomException(message="This is a triggered custom exception", status_code=400)
        return {"name": "FastAPI", "version": "0.103.0", "status": "awesome"}

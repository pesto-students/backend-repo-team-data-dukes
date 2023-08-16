from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

def mount_exception_handler(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        error_messages = None
        for error in exc.errors():
            error_messages = f"{error['msg']}"
        return JSONResponse(
            status_code=400,
            content={"details": error_messages}
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"details": str(exc)}
        )

    return app


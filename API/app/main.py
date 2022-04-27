from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from api.errors.http_error import http_error_handler
from api.errors.validation_error import http422_error_handler
from api.routes.api import router
from config import APP_NAME, APP_VERSION


def get_application() -> FastAPI:
    application = FastAPI(title=APP_NAME, version=APP_VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(router, prefix="/fsec/api/v1")
    return application


app = get_application()

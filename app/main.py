import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.core.config import PROJECT_NAME, ALLOWED_HOSTS, VERSION, API_PREFIX
from app.api.routes.api import router as api_router
from fastapi.exceptions import RequestValidationError
import pathlib

dir_path = pathlib.Path.cwd()


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, version=VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = get_application()

from fastapi import FastAPI
from rq import Queue
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
import pathlib
from API.Discovery.app.api.errors.http_error import http_error_handler
from API.Discovery.app.api.errors.validation_error import http422_error_handler
from API.Discovery.app.api.routes.api import router as api_router
from API.Discovery.app.core.config import settings
from API.Discovery.app.worker import conn

dir_path = pathlib.Path.cwd()
rq_que = Queue(name='discovery_api', connection=conn)


def get_application() -> FastAPI:
    application = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router, prefix="/fsec/api/v1")
    return application


app = get_application()

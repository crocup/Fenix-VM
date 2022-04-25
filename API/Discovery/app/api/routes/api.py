from fastapi import APIRouter
from API.Discovery.app.api.routes import discovery

router = APIRouter()
router.include_router(discovery.router, tags=["discovery"], prefix="/discovery")

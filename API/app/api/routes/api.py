from fastapi import APIRouter
from api.routes import discovery, scanner

router = APIRouter()
router.include_router(discovery.router, tags=["discovery"], prefix="/discovery")
router.include_router(scanner.router, tags=["scanner"], prefix="/scanner")

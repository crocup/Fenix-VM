from fastapi import APIRouter
from rq import Queue
from app.api.routes import discovery, rqtask, scanner
from app.worker import conn

router = APIRouter()
rq_que = Queue(name='fsec', connection=conn)
router.include_router(discovery.router, tags=["discovery"], prefix="/discovery")
router.include_router(rqtask.router, tags=["task"], prefix="/task")
router.include_router(scanner.router, tags=["scanner"], prefix="/scanner")
router.include_router(scanner.router, tags=["feeds"], prefix="/feeds")
router.include_router(scanner.router, tags=["setting"], prefix="/setting")

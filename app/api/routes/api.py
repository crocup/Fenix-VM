from fastapi import APIRouter
from rq import Queue
from app.api.routes import discovery, rqtask, scanner
from worker import conn

router = APIRouter()
rq_que = Queue(name='fsec', connection=conn)
router.include_router(discovery.router, tags=["hostdiscover"], prefix="/discovery")
router.include_router(rqtask.router, tags=["task"], prefix="/task")
router.include_router(scanner.router, tags=["task"], prefix="/scanner")

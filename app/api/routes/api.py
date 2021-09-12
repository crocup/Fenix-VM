from fastapi import APIRouter
from rq import Queue
from app.api.routes import hostdiscover, rqtask
from worker import conn

router = APIRouter()
rq_que = Queue(name='fsec', connection=conn)
router.include_router(hostdiscover.router, tags=["hostdiscover"], prefix="/discovery")
router.include_router(rqtask.router, tags=["task"], prefix="/task")

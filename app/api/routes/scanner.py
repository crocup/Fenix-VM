from fastapi import APIRouter
from app.models.hostid import HostIn, HostOut

router = APIRouter()


@router.post("/start_task")
async def get_start_scanner(host: HostIn):
    pass
    # from app.api.routes.api import rq_que
    # job = rq_que.enqueue_call(
    #     func=result_discovery, args=(HostDiscovery(host.host),)
    # )
    return HostOut(status=True, job="test")


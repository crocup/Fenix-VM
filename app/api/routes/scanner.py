from fastapi import APIRouter
from starlette import status
from app.models.hostid import HostIn, HostOut

router = APIRouter()


@router.post("/start_task", status_code=status.HTTP_200_OK, name="scanner:start",)
async def start_scanner(host: HostIn):
    # from app.api.routes.api import rq_que
    # job = rq_que.enqueue_call(
    #     func=result_discovery, args=(HostDiscovery(host.host),)
    # )
    return HostOut(status=True, job="test")

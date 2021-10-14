from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.post("/start_task", status_code=status.HTTP_200_OK, name="scanner:start",)
async def start_scanner():
    pass
    # from app.api.routes.api import rq_que
    # job = rq_que.enqueue_call(
    #     func=result_discovery, args=(HostDiscovery(host.host),)
    # )
    # return HostOut(status=True, job="test")

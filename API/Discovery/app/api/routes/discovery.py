import logging
from fastapi import APIRouter
from starlette import status
from API.Discovery.app.core.scanner import result_scan
from API.Discovery.app.models.model import Host, Result
from API.Discovery.app.service.discovery import HostDiscovery
from API.Discovery.app.service.network import check_ip

router = APIRouter()


@router.post("/start", status_code=status.HTTP_200_OK, name="discovery:start", )
async def start_task_discovery(host: Host):
    try:
        if check_ip(host.host):
            from API.Discovery.app.main import rq_que
            job = rq_que.enqueue_call(
                func=result_scan,
                args=(HostDiscovery(host=host.host),))
            return Result(success=True)
        return Result(success=False)
    except Exception as e:
        logging.error(e)
        return Result(success=False)

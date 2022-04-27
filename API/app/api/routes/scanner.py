import logging
from fastapi import APIRouter
from starlette import status
from model import Host, Result
from network import check_ip
from sender import result_sender, HostSenderData

router = APIRouter()


@router.post("/start", status_code=status.HTTP_200_OK, name="scanner:start", )
async def start_task_scanner(host: Host):
    try:
        if check_ip(host.host):
            result_sender(HostSenderData(data=host.json(), rabbit_queue="Scanner"))
            return Result(success=True)
        return Result(success=False)
    except Exception as e:
        logging.error(e)
        return Result(success=False)
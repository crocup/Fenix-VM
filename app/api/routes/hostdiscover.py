from fastapi import APIRouter
from app.models.hostid import Host
from app.services.hostdiscovery import result_scanner, HostDiscovery

router = APIRouter()


@router.get("/get_page")
async def get_page():
    return {"success": True}


@router.post("/start_task")
async def get_start_discovery(host: Host):
    """

    """
    from app.api.routes.api import rq_que
    job = rq_que.enqueue_call(
        func=result_scanner, args=(HostDiscovery(host.host),)
    )
    return {"success": True, "id": job.id}

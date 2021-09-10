from fastapi import APIRouter
from rq.job import Job
from app.services.hostdiscovery import result_scanner, HostDiscovery
from worker import conn

router = APIRouter()


@router.get("/get_page")
async def get_page():
    return {"success": True}


@router.post("/start_task")
async def get_start_discovery():
    # if not request.json or not 'host' in request.json:
    #     abort(400)
    # data = request.get_json()
    # job = q.enqueue_call(
    #     func=result_scanner, args=(HostDiscovery(data["host"]),), result_ttl=500
    # )
    from app.api.routes.api import rq_que
    job = rq_que.enqueue_call(
        func=result_scanner, args=(HostDiscovery("192.168.100.61"),), result_ttl=500
    )
    return {"success": True, "id": job.id}


@router.get("/{job_key}")
async def status_discovery(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return {"success": True, "id": job_key}
    else:
        return {"success": False}

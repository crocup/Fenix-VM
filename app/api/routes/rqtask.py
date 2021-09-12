from fastapi import APIRouter
from rq.job import Job
from worker import conn

router = APIRouter()


@router.get("/{job_key}")
async def status_task(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return {"success": True, "id": job_key}
    else:
        return {"success": False}

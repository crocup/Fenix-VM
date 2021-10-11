import rq.exceptions
from fastapi import APIRouter
from rq.job import Job
from starlette import status
from app.models.task import Task
from worker import conn

router = APIRouter()


@router.get("/", status_code=status.HTTP_204_NO_CONTENT, name="task:default",)
async def status_default():
    return Task(success=False)


@router.get("/{job_key}", status_code=status.HTTP_200_OK, name="task:status",)
async def status_task(job_key):
    try:
        job = Job.fetch(job_key, connection=conn)
        if job.is_finished:
            return Task(success=True)
        else:
            return Task(success=False)
    except rq.exceptions.NoSuchJobError:
        return Task(success=False)

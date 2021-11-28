import rq.exceptions
from fastapi import APIRouter
from rq.job import Job
from starlette import status
from app.models.task import Status
from app.worker import conn

router = APIRouter()


@router.get("/", status_code=status.HTTP_204_NO_CONTENT, name="task:default",)
async def status_default():
    """

    """
    return Status(success=False, message="no content")


@router.get("/{job_key}", status_code=status.HTTP_200_OK, name="task:status",)
async def status_task(job_key):
    """

    """
    try:
        job = Job.fetch(job_key, connection=conn)
        if job.is_finished:
            return Status(success=True, message="job finished")
        else:
            return Status(success=False, message="job is not finished")
    except rq.exceptions.NoSuchJobError:
        return Status(success=False, message="no such job")

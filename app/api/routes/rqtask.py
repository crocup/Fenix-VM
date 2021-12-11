import rq.exceptions
from fastapi import APIRouter
from rq.job import Job
from starlette import status
from app.models.task import Result
from app.worker import conn

router = APIRouter()


@router.get("/", status_code=status.HTTP_204_NO_CONTENT, name="task:default",)
async def status_default():
    """

    """
    return Result(success=False)


@router.get("/{job_key}", status_code=status.HTTP_200_OK, name="task:status",)
async def status_task(job_key):
    """

    """
    try:
        job = Job.fetch(job_key, connection=conn)
        if job.is_finished:
            return Result(success=True)
        else:
            return Result(success=False)
    except rq.exceptions.NoSuchJobError:
        return Result(success=False)

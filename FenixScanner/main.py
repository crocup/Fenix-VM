from fastapi import FastAPI
from rq import Queue
from worker import conn
from pydantic import BaseModel

# use FastAPI
app = FastAPI()
# RQ Worker
q_fenix_scan = Queue(name='scanner', connection=conn)


class Host(BaseModel):
    host: str


@app.post("/api/v1/fenix/scanner")
async def read_root(item: Host):
    """
    send to core job_id
    return: JSON job.id
    """
    # job = q_fenix_scan.enqueue_call(
    #     func=DistributionDB(item.host).template_db, args=()
    # )
    # return {"job.id": job.id}
    pass

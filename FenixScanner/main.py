from fastapi import FastAPI
from host_discovery import *
from rq import Queue
from worker import conn
from pydantic import BaseModel

app = FastAPI()
q_fenix_scan = Queue(name='scan', connection=conn)


class Host(BaseModel):
    host: str


@app.post("/api/v1/fenix/hostdiscovery")
async def read_root(item: Host):
    """
    send to core job_id
    """

    send_to_db = DistributionDB(item.host)
    job = q_fenix_scan.enqueue_call(
        func=send_to_db.template_db, args=()
    )
    return {"job.id": job.id}


@app.post("/api/v1/fenix/scanner")
async def read_scanner(item: Host):
    """
    send to core job_id
    """
    pass

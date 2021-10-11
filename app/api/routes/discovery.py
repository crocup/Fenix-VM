from fastapi import APIRouter
from starlette import status
from app.core.config import DATABASE_PORT, DATABASE_IP
from app.models.hostid import HostIn, HostOut
from app.models.task import TaskResult
from app.services.database import MessageProducer, MongoDriver
from app.services.hostdiscovery import result_discovery, HostDiscovery

router = APIRouter()


@router.get("/get", status_code=status.HTTP_200_OK, name="discovery:get",)
async def get_page():
    """

    """
    host_discovery_data = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                      base="HostDiscovery", collection="result"))
    db_list = list()
    for doc in host_discovery_data.get_all_message():
        del doc["_id"]
        db_list.append(doc)
    return TaskResult(status=True, data=db_list)


@router.post("/start_task", status_code=status.HTTP_200_OK, name="discovery:start",)
async def get_start_discovery(host: HostIn):
    """

    """
    from app.api.routes.api import rq_que
    job = rq_que.enqueue_call(
        func=result_discovery, args=(HostDiscovery(host.host),)
    )
    return HostOut(status=True, job=job.id)

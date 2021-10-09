from fastapi import APIRouter
from app.core.config import DATABASE_PORT, DATABASE_IP
from app.models.hostid import HostIn, Discovery, HostOut
from app.services.database import MessageProducer, MongoDriver
from app.services.hostdiscovery import result_discovery, HostDiscovery

router = APIRouter()


@router.get("/get_page")
async def get_page():
    """

    """
    host_discovery_data = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                      base="HostDiscovery", collection="result"))
    db_list = [doc for doc in host_discovery_data.get_all_message()]
    print(db_list)
    return Discovery(status=True, data=db_list)


@router.post("/start_task")
async def get_start_discovery(host: HostIn):
    """

    """
    from app.api.routes.api import rq_que
    job = rq_que.enqueue_call(
        func=result_discovery, args=(HostDiscovery(host.host),)
    )
    return HostOut(status=True, job=job.id)

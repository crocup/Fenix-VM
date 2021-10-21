from fastapi import APIRouter
from starlette import status
from datetime import datetime
from app.core.config import DATABASE_PORT, DATABASE_IP
from app.core.scanner import result_scan
from app.models.task import GetResult, Start, Create, Status
from app.services.database import MessageProducer, MongoDriver
from app.services.hostdiscovery import HostDiscovery

router = APIRouter()


@router.post("/get_task", status_code=status.HTTP_200_OK, name="discovery:get", )
async def get_page(task: Start):
    """
    список всех хостов в задаче
    """
    try:
        host_discovery_data = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                          base="HostDiscovery", collection="result"))
        db_list = list()
        for doc in host_discovery_data.get_message({"name": task.name}):
            db_list.append(doc)
        return GetResult(status=True, data=db_list)
    except Exception as e:
        return GetResult(status=False, data=[])


@router.post("/create_task", status_code=status.HTTP_200_OK, name="discovery:create", )
async def create_task_discovery(task: Create):
    """
    создаем задачу для обнаружения хостов
    данные сохраняются в бд
    """
    try:
        db_discovery_create_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                               base="HostDiscovery", collection="task"))
        message = {
            "mask": task.mask,
            "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
            "name": task.name,
        }
        db_discovery_create_task.update_message(message, {"name": task.name})
        return Status(success=True, message="insert data")
    except Exception as e:
        return Status(success=False, message=e)


@router.post("/start_task", status_code=status.HTTP_200_OK, name="discovery:start", )
async def start_task_discovery(task: Start):
    """
    запускаем задачу обнаружения хостов
    данные читаются из БД
    """
    try:
        db_discovery_start_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                              base="HostDiscovery", collection="task"))
        host_db = db_discovery_start_task.get_message({"name": task.name})
        for host in host_db:
            host_db = host
        from app.api.routes.api import rq_que
        job = rq_que.enqueue_call(
            func=result_scan, args=(HostDiscovery(host=host_db['mask'], name=host_db['name'], db="HostDiscovery",
                                                  table="result"),)
        )
        return Status(success=True, message=job.id)
    except Exception as e:
        return Status(success=False, message=e)

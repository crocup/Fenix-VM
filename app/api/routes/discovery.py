from fastapi import APIRouter
import logging
from starlette import status
from app.core.config import DATABASE_PORT, DATABASE_IP, BASE_VM, COLLECTION_HOST_DISCOVERY
from app.core.scanner import result_scan
from app.models.discovery import Host, ResultTask, Result
from app.services.database import MessageProducer, MongoDriver
from app.services.hostdiscovery import HostDiscovery
from app.core.setting import Settings

router = APIRouter()


@router.post("/start", status_code=status.HTTP_200_OK, name="discovery:start", )
async def start_task_discovery():
    """
    запуск задачи
    """
    try:
        from app.api.routes.api import rq_que
        job = rq_que.enqueue_call(
            func=result_scan,
            args=(HostDiscovery(host=Settings().MASK, db=BASE_VM,
                                table=COLLECTION_HOST_DISCOVERY),)
        )
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)


@router.get("/results", status_code=status.HTTP_200_OK, name="discovery:tasks", )
async def tasks_discovery():
    """
    список всех задач
    """
    try:
        db_discovery_start_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                              base=BASE_VM,
                                                              collection=COLLECTION_HOST_DISCOVERY))
        name = db_discovery_start_task.get_all_message()
        db_list = list()
        for i in name:
            del i["_id"]
            db_list.append(i)
        return ResultTask(status=True, data=db_list)
    except Exception as e:
        logging.error(e)
        return ResultTask(status=False, data=[])


@router.delete("/delete", status_code=status.HTTP_200_OK, name="discovery:delete", )
async def delete_task_discovery(host: Host):
    """
    удалить задачу
    """
    try:
        db_discovery_delete_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                               base=BASE_VM,
                                                               collection=COLLECTION_HOST_DISCOVERY))
        db_discovery_delete_task.delete_message({"host": host.host})
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)

from fastapi import APIRouter
import logging
from starlette import status
from datetime import datetime
from app.core.config import DATABASE_PORT, DATABASE_IP
from app.core.scanner import result_scan
from app.models.discovery import Start, ResultTask, Create, Edit, Result
from app.services.database import MessageProducer, MongoDriver
from app.services.hostdiscovery import HostDiscovery
import uuid

router = APIRouter()


@router.post("/create", status_code=status.HTTP_200_OK, name="discovery:create", )
async def create_task_discovery(task: Create):
    """
    создать задачу
    """
    try:
        db_discovery_create_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                               base="HostDiscovery", collection="task"))
        message = {
            "mask": task.mask,
            "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
            "name": task.name,
        }
        db_discovery_create_task.update_message({"uuid": str(uuid.uuid4())}, message)
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)


@router.post("/start", status_code=status.HTTP_200_OK, name="discovery:start", )
async def start_task_discovery(task: Start):
    """
    запуск задачи
    """
    try:
        db_discovery_start_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                              base="HostDiscovery", collection="task"))
        host_db = db_discovery_start_task.get_message({"uuid": task.uuid})
        for host in host_db:
            host_db = host
        from app.api.routes.api import rq_que
        job = rq_que.enqueue_call(
            func=result_scan,
            args=(HostDiscovery(host=host_db['mask'], uuid=host_db['uuid'], name=host_db['name'], db="HostDiscovery",
                                table="result"),)
        )
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)


@router.post("/result", status_code=status.HTTP_200_OK, name="discovery:get", )
async def get_page(task: Start):
    """
    получение информации по задаче
    """
    try:
        host_discovery_data = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                          base="HostDiscovery", collection="result"))
        db_list = list()
        for doc in host_discovery_data.get_message({"uuid": task.uuid}):
            db_list.append(doc)
        return ResultTask(status=True, data=db_list)
    except Exception as e:
        logging.error(e)
        return ResultTask(status=False, data=[])


@router.get("/tasks", status_code=status.HTTP_200_OK, name="discovery:tasks", )
async def tasks_discovery():
    """
    список всех задач
    """
    try:
        db_discovery_start_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                              base="HostDiscovery", collection="task"))
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
async def delete_task_discovery(task: Start):
    """
    удалить задачу
    """
    try:
        db_discovery_delete_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                               base="HostDiscovery", collection="task"))
        db_discovery_delete_task.delete_message({"uuid": task.uuid})
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)


@router.put("/edit", status_code=status.HTTP_200_OK, name="discovery:edit", )
async def edit_task_discovery(task: Edit):
    """
    удалить все задачи
    """
    try:
        db_discovery_edit_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                             base="HostDiscovery", collection="task"))
        if task.name is None:
            message = {"name": task.name, "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y")}
        elif task.mask is None:
            message = {"mask": task.mask, "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y")}
        else:
            message = {
                "name": task.name,
                "mask": task.mask,
                "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y")
            }
        db_discovery_edit_task.update_message({"uuid": task.uuid}, message)
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)

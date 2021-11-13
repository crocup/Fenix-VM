from fastapi import APIRouter
import logging
from starlette import status
from datetime import datetime
from app.core.config import DATABASE_IP, DATABASE_PORT
from app.core.scanner import result_scan
from app.models.task import Create, Status, Start, GetResult
from app.services.database import MessageProducer, MongoDriver
from app.services.scanner import ServiceDetection

router = APIRouter()


@router.post("/start_task", status_code=status.HTTP_200_OK, name="scanner:start", )
async def start_scanner(task: Start):
    try:
        db_scanner_start_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                            base="Scanner", collection="task"))
        host_db = db_scanner_start_task.get_message({"name": task.name})
        for host in host_db:
            host_db = host
        from app.api.routes.api import rq_que
        job = rq_que.enqueue_call(
            func=result_scan, args=(ServiceDetection(host=host_db['mask'], name=host_db['name'], db="Scanner",
                                                     table="result"),)
        )
        return Status(success=True, message=job.id)
    except Exception as e:
        logging.error(e)
        return Status(success=False, message=e)


@router.post("/create_task", status_code=status.HTTP_200_OK, name="scanner:create", )
async def create_task_scanner(task: Create):
    try:
        db_scanner_create_task = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                             base="Scanner", collection="task"))
        message = {
            "mask": task.mask,
            "date": datetime.now().strftime("%H:%M:%S %d.%m.%Y"),
            "name": task.name,
        }
        db_scanner_create_task.update_message({"name": task.name}, message)
        return Status(success=True, message="insert data")
    except Exception as e:
        logging.error(e)
        return Status(success=False, message=f"error: {e}")


@router.post("/get_task", status_code=status.HTTP_200_OK, name="scanner:get", )
async def get_page_scanner(task: Start):
    try:
        scan_data = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                base="Scanner", collection="result"))
        db_list = list()
        for doc in scan_data.get_message({"name": task.name}):
            result = {
                "host": doc['host'],
                "name": task.name,
                "time": doc['time']
            }
            db_list.append(result)
        return GetResult(status=True, data=db_list)
    except Exception as e:
        logging.error(e)
        return GetResult(status=False, data=[])

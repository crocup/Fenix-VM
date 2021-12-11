from fastapi import APIRouter
import logging
from starlette import status
from app.core.config import DATABASE_IP, DATABASE_PORT, BASE_VM, COLLECTION_HOST_DISCOVERY, COLLECTION_SCANNER
from app.core.scanner import result_scan
from app.models.scanner import Result
from app.services.database import MessageProducer, MongoDriver
from app.services.scanner import ServiceDetection

router = APIRouter()


@router.post("/start", status_code=status.HTTP_200_OK, name="scanner:start", )
async def start_scanner():
    """Запуск сканирования"""
    try:
        db_scanner_get_ip = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                        base=BASE_VM, collection=COLLECTION_HOST_DISCOVERY))
        host_name = db_scanner_get_ip.get_all_message()
        for host in host_name:
            from app.api.routes.api import rq_que
            job = rq_que.enqueue_call(
                func=result_scan, args=(ServiceDetection(host=host["host"],
                                                         db=BASE_VM, table=COLLECTION_SCANNER),), timeout=600)
        return Result(success=True)
    except Exception as e:
        logging.error(e)
        return Result(success=False)

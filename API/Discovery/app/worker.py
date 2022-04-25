"""
Worker для выполнения фоновых заданий
"""
import redis
from rq import Worker, Queue, Connection
from starlette.config import Config

listen = ['discovery_api']
config = Config(".env")
REDIS_IP: str = config("REDIS_IP", default="localhost")
REDIS_PORT: int = config("REDIS_PORT", default=6379)
redis_url = 'redis://'+REDIS_IP+':'+str(REDIS_PORT)
conn = redis.from_url(redis_url)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()

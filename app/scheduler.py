import schedule
import time
from app.main import host_discovery

schedule.every(1).minutes.do(host_discovery)
while True:
    schedule.run_pending()
    time.sleep(1)

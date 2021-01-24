import schedule
import time
from app.main import inventory

schedule.every(1).minutes.do(inventory)
while True:
    schedule.run_pending()
    time.sleep(1)

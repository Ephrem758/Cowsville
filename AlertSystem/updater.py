import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from .sendMesage import schedule_api

logging.basicConfig(level=logging.INFO)

def start():
    jobstores = {'default': MemoryJobStore()}
    executors = {'default': ThreadPoolExecutor(2)}
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
    
    scheduler.add_job(schedule_api, 'interval', minutes=1)
    logging.info("Scheduler started")
    
    scheduler.start()

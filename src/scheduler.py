from apscheduler.schedulers.background import BackgroundScheduler
from src.utils import bot


def tick():
    pass


scheduler = BackgroundScheduler()
scheduler.add_job(tick, 'interval', seconds=5)

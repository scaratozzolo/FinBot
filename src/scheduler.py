from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from src.schedules.swings import check_swings
from src.schedules.earnings import get_upcoming_earnings


scheduler = BackgroundScheduler(timezone=ZoneInfo("America/New_York"))
scheduler.add_job(check_swings, 'interval', minutes=30)
scheduler.add_job(get_upcoming_earnings, 'cron', day_of_week=6, hour=9)

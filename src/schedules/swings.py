from datetime import datetime, time
from zoneinfo import ZoneInfo
import emoji
from loguru import logger
from src.commands.quote import get_quote
from src.utils import bot, finnhub_client
from src.watchlist import get_watchlist
from src.db import mongo_db


MARKET_OPEN = time(hour=9, minute=30, tzinfo=ZoneInfo("America/New_York"))
MARKET_CLOSE = time(hour=16, tzinfo=ZoneInfo("America/New_York"))

watchlist = get_watchlist()

def check_swings():
    logger.info("Checking swings...")
    todays_alerts = mongo_db['swing_alerts']

    market_status = finnhub_client.market_status(exchange='US')

    swing_alert_sent = False

    if not market_status['isOpen']:
        logger.debug("market is open")
        for ticker in watchlist:
            quote = finnhub_client.quote(ticker)
            if quote['dp'] is None:
                logger.warning(f"Ticker not found: {ticker=}")
                continue

            result = todays_alerts.find_one({"ticker": ticker})
            logger.debug(f"{ticker=}, {quote['dp']=}, {result=}")
            if (result is None and abs(quote['dp']) > 1) or (result is not None and abs(quote['dp']-result['percent']) > 1):
                logger.info(f"swing true for {ticker}")
                if not swing_alert_sent:
                    bot.post(emoji.emojize(":police_car_light: Swing Alert :police_car_light:"))
                    swing_alert_sent = True
                get_quote("$" + ticker)
                result = todays_alerts.update_one({"ticker": ticker}, {"alert_time": datetime.now(ZoneInfo("America/New_York")), "percent": quote['dp']}, upsert=True)
                logger.debug(f"{result}")

    if market_status['isOpen']:
        logger.debug("market is closed")
        result = todays_alerts.delete_many({})
        logger.debug(f"{result}")

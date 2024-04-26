from datetime import datetime, time
from zoneinfo import ZoneInfo
import emoji
from loguru import logger
from src.commands.quote import get_quote
from src.utils import bot, finnhub_client
from src.watchlist import watchlist


MARKET_OPEN = time(hour=9, minute=30, tzinfo=ZoneInfo("America/New_York"))
MARKET_CLOSE = time(hour=16, tzinfo=ZoneInfo("America/New_York"))

todays_alerts = {}

def check_swings():
    logger.info("Checking swings...")
    global todays_alerts
    swings = []

    market_status = finnhub_client.market_status(exchange='US')

    if market_status['isOpen']:
        logger.debug("market is open")
        for ticker in watchlist:
            quote = finnhub_client.quote(ticker)
            if quote['dp'] is None:
                logger.warning(f"Ticker not found: {ticker=}")
            
            if abs(quote['dp']) > 1:
                logger.debug(f"{ticker=}, {quote['dp']=}")
                swings.append(ticker)

        to_send = [f"${i}" for i in swings if f"${i}" not in todays_alerts]
        logger.debug(f"{to_send=}")
        if len(to_send) > 0:
            bot.post(emoji.emojize(":police_car_light: Swing Alert :police_car_light:"))
            get_quote(" ".join(to_send))
            for i in to_send:
                todays_alerts[i] = datetime.now()

    if not market_status['isOpen']:
        logger.debug("market is closed")
        todays_alerts = {}

    logger.debug(f"{todays_alerts=}")
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import emoji
import yfinance as yf
from loguru import logger
from src.utils import bot, finnhub_client
from src.watchlist import get_watchlist


def get_upcoming_earnings():
    logger.info("Getting earnings")

    from_date = datetime.now(tz=ZoneInfo("America/New_York"))
    from_date_str = from_date.strftime("%Y-%m-%d")
    to_date = from_date + timedelta(days=7)
    to_date_str = to_date.strftime("%Y-%m-%d")
    logger.debug(f"checking earnings {from_date=} {to_date=}")

    msg = emoji.emojize("Upcoming Earnings :calendar:\n\n")
    earnings_cal = {}
    send_message = False
    for ticker in get_watchlist():
        cal = finnhub_client.earnings_calendar(
            _from=from_date_str, to=to_date_str, symbol=ticker
        )["earningsCalendar"]
        if cal != []:
            logger.info(f"{ticker} has upcoming earnings")
            send_message = True
            earnings_date = datetime.strptime(cal[0]["date"], "%Y-%m-%d")
            logger.debug(f"{ticker} {earnings_date=}")

            if cal[0]["hour"] == "amc":
                when = "After Market Close"
            elif cal[0]["hour"] == "bmo":
                when = "Before Market Open"
            else:
                when = ""
            logger.debug(f"{ticker} {when=}")

            try:
                yf_ticker = yf.Ticker(ticker).info
                ticker_name = yf_ticker["shortName"]
                ticker_msg = f"{ticker_name} ({ticker})" + "\n"
            except Exception as excp:
                logger.warning(excp)
                ticker_msg = ticker + "\n"
            
            ticker_msg += f"{earnings_date.strftime('%A, %B %d')} {when}\n\n"

            earnings_cal[ticker] = {"date": earnings_date, "msg": ticker_msg}

    if send_message:
        logger.info("Sending upcoming earnings")
        earnings_cal = {
            k: v
            for k, v in sorted(earnings_cal.items(), key=lambda item: item[1]["date"])
        }
        for _, i in earnings_cal.items():
            msg += i["msg"]
        bot.post(msg)
    else:
        logger.debug("no earnings to send")

import re
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
from loguru import logger
from src.utils import bot, finnhub_client
import emoji


def get_quote(msg):
    logger.debug("inside get_quote")

    try:
        tickers = re.findall(r"\$\^?[a-zA-Z.]+-?[a-zA-Z.]*", msg)
        tickers = [ticker[1:].upper() for ticker in tickers]
        logger.debug(tickers)

        for ticker in tickers:
            try:
                quote = finnhub_client.quote(ticker)
                if quote['dp'] is None:
                    raise ValueError(f"Ticker not found: {ticker=}")
                try:
                    yf_ticker = yf.Ticker(ticker).info
                    ticker_name = yf_ticker["shortName"]
                except Exception as excp:
                    logger.error(excp)
                    ticker_name = ticker
                replymsg = emoji.emojize(f"{ticker_name} Quote {':chart_increasing:' if quote['dp'] > 0 else ':chart_decreasing:'}\nPrice: ${quote['c']}\nDollar Change: {quote['d']}\n% Change: {quote['dp']}%", language='alias')
                if 't' in quote:
                    dt = datetime.fromtimestamp(quote['t'], tz=ZoneInfo('UTC'))
                    replymsg += f"\nChange since {dt.astimezone(ZoneInfo('America/New_York')).strftime('%B %d, %Y %I:%M %p')}"
                bot.post(replymsg)
                logger.debug(f"bot posted quote for {ticker}")
            except Exception as e:
                logger.error(e)
                bot.post(f"Error encountered for ${ticker}")

        logger.debug("get_quote finished")
    except Exception as e:
        logger.exception(e)

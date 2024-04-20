import re
from datetime import date, timedelta
import pandas as pd
import yfinance as yf
from loguru import logger
from src.utils import bot


def get_quote(msg):
    logger.debug("inside get_quote")

    try:
        tickers = re.findall(r"\$\^?[a-zA-Z.]+-?[a-zA-Z.]*", msg)
        tickers = [ticker[1:].upper() for ticker in tickers]
        logger.debug(tickers)

        data = yf.download(tickers, start=date.today() - timedelta(days=7))["Adj Close"]
        print(data)
        if isinstance(data, pd.DataFrame):
            logger.debug(f"df rows {len(data)}, cols {data.columns}")
            data = data.dropna(axis=1, how="all")
            logger.debug(f"df rows {len(data)}, cols {data.columns}")
        else:
            logger.debug(f"series rows {len(data)}")

        quote = data.iloc[-1].round(2)
        logger.debug(f"{quote=}")
        pchange = (data.pct_change().dropna().iloc[-1] * 100).round(2)
        logger.debug(f"{pchange=}")
        dchange = (data.iloc[-1] - data.iloc[-2]).round(2)
        logger.debug(f"{dchange=}")

        if len(tickers) < 2:
            logger.debug("1 ticker")
            yf_ticker = yf.Ticker(tickers[0]).info
            try:
                ticker_name = yf_ticker["shortName"]
            except Exception as excp:
                logger.error(excp)
                ticker_name = tickers[0]
            replymsg = f"{ticker_name} Quote:\nPrice: ${quote}\nDollar Change: {dchange}\n% Change: {pchange}%"
            bot.post(replymsg)
            logger.debug("bot posted quote for single ticker")
        else:
            logger.debug(f"{len(tickers)=}")
            for ticker in tickers:
                try:
                    yf_ticker = yf.Ticker(ticker).info
                    try:
                        ticker_name = yf_ticker["shortName"]
                    except Exception as excp:
                        logger.error(excp)
                        ticker_name = ticker
                    replymsg = f"{ticker_name} Quote:\nPrice: ${quote[ticker]}\nDollar Change: {dchange[ticker]}\n% Change: {pchange[ticker]}%"
                    bot.post(replymsg)
                    logger.debug(f"bot posted quote for {ticker}")
                except Exception as e:
                    logger.exception(e)
                    bot.post(f"Error encountered for ${ticker}")

        logger.debug("get_quote finished")
    except Exception as e:
        logger.exception(e)

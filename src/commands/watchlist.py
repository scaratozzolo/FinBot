import emoji
import yfinance as yf
from loguru import logger
from src.watchlist import add_watchlist, remove_watchlist, get_watchlist
from src.models import Commands
from src.utils import bot


def handle_watchlist(msg, user_info):
    msg_split = msg.split()
    logger.debug(f"{msg_split}")
    if len(msg_split) == 1:
        logger.info("getting watchlist")
        watchlist = get_watchlist()
        reply_msg = emoji.emojize("Watchlist :eyes: \n\n")
        for i in watchlist:
            reply_msg += f"{i}\n"

        bot.post(reply_msg)
    elif len(msg_split) == 2:
        ticker = msg_split[-1].upper()

        try:
            yf_ticker = yf.Ticker(ticker).info
            ticker_name = yf_ticker["shortName"]
        except Exception as excp:
            logger.error(excp)
            ticker_name = ticker

        logger.info("adding to watchlist")
        add_result = add_watchlist(ticker, user_info)
        if add_result:
            logger.info("added to watchlist")
            if ticker_name != ticker:
                bot.post(emoji.emojize(f":plus: {ticker_name} ({ticker}) added to watchlist."))
            else:
                bot.post(emoji.emojize(f":plus: {ticker} added to watchlist."))

        else:
            logger.info("already in watchlist, removing from watchlist")
            remove_watchlist(ticker)
            if ticker_name != ticker:
                bot.post(emoji.emojize(f":minus: {ticker_name} ({ticker}) removed from watchlist."))
            else:
                bot.post(emoji.emojize(f":minus: {ticker} removed from watchlist."))

    else:
        bot.post(Commands.WATCHLIST.value.usage)

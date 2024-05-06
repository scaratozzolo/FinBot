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
    elif len(msg_split) == 3:
        ticker = msg_split[2].upper()

        if msg_split[1].lower() == "add":
            logger.info("adding to watchlist")
            add_watchlist(ticker, user_info)
            try:
                yf_ticker = yf.Ticker(ticker).info
                ticker_name = yf_ticker["shortName"]
                bot.post(emoji.emojize(f":plus: {ticker_name} ({ticker}) added to watchlist."))
            except Exception as excp:
                logger.warning(excp)
                bot.post(emoji.emojize(f":plus: {ticker} added to watchlist."))

        elif msg_split[1].lower() == "remove":
            logger.info("removing from watchlist")
            remove_watchlist(ticker)
            bot.post(emoji.emojize(f":minus: {ticker} removed from watchlist."))

        else:
            bot.post(Commands.WATCHLIST.value.usage)

    else:
        bot.post(Commands.WATCHLIST.value.usage)

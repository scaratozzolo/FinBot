from loguru import logger
from src.db import mongo_db


watchlist_collection = mongo_db["watchlist"]
watchlist = ["BTC-USD", "LTC-USD", "NVDA", "SPY", "QQQ", "RIOT", "MCD", "LLY"]


def get_watchlist():
    result = watchlist_collection.find().sort("ticker")

    return [i["ticker"] for i in result]


def add_watchlist(ticker, user_info):
    ticker_exists = watchlist_collection.find_one({"ticker": ticker})
    logger.debug(f"{ticker_exists=}")

    if not ticker_exists:
        result = watchlist_collection.insert_one(
            {
                "ticker": ticker,
                "user_info": user_info,
            }
        )

        logger.debug(f"{result}")


def remove_watchlist(ticker):
    result = watchlist_collection.delete_one({"ticker": ticker})

    logger.debug(f"{result}")

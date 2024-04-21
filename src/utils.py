from loguru import logger
from fastapi import HTTPException
from groupy.client import Client
from groupy.api.bots import Bots, Bot
import finnhub
from src.config import config

client = Client.from_token(config.groupme_access_token)


def get_bot() -> Bot:
    # TODO probably find a better way to do this, like use bot id
    bot_manger = Bots(client.session)
    bot = None
    for i in bot_manger.list():
        logger.debug(f"{i=}")
        if i.bot_id == config.bot_id:
            bot = i
            break
    
    if not bot:
        logger.error(f"Bot with {config.bot_id=} could not be found.")
        return

    logger.info(bot)

    return bot

def get_finnhub_client() -> finnhub.Client:
    return finnhub.Client(api_key=config.finnhub_api_key)


async def check_query_token(token: str):
    if token != config.request_token:
        raise HTTPException(status_code=400, detail="Incorrect token provided")


bot = get_bot()
finnhub_client = get_finnhub_client()

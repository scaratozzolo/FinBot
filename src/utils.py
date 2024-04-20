from loguru import logger
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
    if bot is None:
        bot = bot_manger.create(
            config.botname, group_id=config.group_id, callback_url=config.callback_url
        )
        logger.debug("bot created")

    logger.info(bot)

    return bot


def get_group_name() -> str:
    group_name = None
    groups = list(client.groups.list_all())
    for group in groups:
        if group.id == config.group_id:
            group_name = group.name
            break
    logger.debug(group_name)

    return group_name


def get_finnhub_client() -> finnhub.Client:
    return finnhub.Client(api_key=config.finnhub_api_key)





bot = get_bot()
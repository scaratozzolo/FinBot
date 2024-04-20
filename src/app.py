import time
import re
from fastapi import FastAPI
from loguru import logger
from src.config import config
from src.utils import get_bot, client
from src.models import GroupMeCallback, Commands

app = FastAPI(
    title=config.botname,
    summary="GroupMe bot to keep you up to date on finance.",
    version=config.version,
)

bot = get_bot()


@app.post("/financialadvisorstest")
async def financialadvisors(request: GroupMeCallback):
    logger.info(f"{request=}")

    if request.name != bot.name:
        msg = request.text
        msg_split = msg.split()
        logger.debug(f"{msg=}")

        if msg == "":
            return "no message text"

        time.sleep(2)

        try:
            if msg == Commands.HELP.value.command:
                logger.debug("calling help_msg")
                Commands.HELP.value.func(bot, Commands)

            elif len(re.findall(r"\$\^?[a-zA-Z.]+", msg)) > 0:
                logger.debug("calling get_quote")
                Commands.QUOTE.value.func(msg, bot)

            elif msg_split[0] == Commands.CHART.value.command:
                logger.debug("calling create_chart")
                Commands.CHART.value.func(msg, bot, client)

            elif msg.lower().find("warren buffett") > -1:
                logger.debug("calling warren")
                bot.post('"Buy the fucking dip" - Warren Buffett')
                logger.debug("bot posted warren")

            elif msg.lower().find("crypto check") > -1:
                logger.debug("calling crypto check")
                Commands.QUOTE.value.func("$BTC-USD $ETH-USD $LTC-USD $XRP-USD", bot)

        except Exception as e:
            logger.exception(e)
            # bot.post(e)
            # TODO something better probably
            bot.post("Something went wrong.")

    return "success"

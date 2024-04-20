import time
import re
from fastapi import FastAPI
from loguru import logger
from src.config import config
from src.utils import get_bot, client
from src.models import GroupMeCallback, Commands
from src.commands.help import help_msg
from src.commands.quote import get_quote
from src.commands.chart import create_chart
from src.commands.news import get_news
from src.commands.monte_carlo import monte_carlo

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
                help_msg(bot, Commands)

            elif len(re.findall(r"\$\^?[a-zA-Z.]+", msg)) > 0:
                logger.debug("calling get_quote")
                get_quote(msg, bot)

            elif msg_split[0] == Commands.CHART.value.command:
                logger.debug("calling create_chart")
                create_chart(msg, bot, client)

            elif msg.lower().find("warren buffett") > -1:
                logger.debug("calling warren")
                bot.post('"Buy the fucking dip" - Warren Buffett')
                logger.debug("bot posted warren")

            elif msg.lower().find("crypto check") > -1:
                logger.debug("calling crypto check")
                get_quote("$BTC-USD $ETH-USD $LTC-USD $XRP-USD", bot)

            elif msg_split[0] == Commands.NEWS.value.command:
                logger.debug("calling get_news")
                get_news(msg, bot)

            elif msg_split[0] == Commands.MC.value.command:
                logger.debug("calling monte_carlo")
                monte_carlo(msg, bot, client)

        except Exception as e:
            logger.exception(e)
            # bot.post(e)
            # TODO something better probably
            bot.post("Something went wrong.")

    return "success"

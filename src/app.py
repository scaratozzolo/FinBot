import time
import re
import random
from fastapi import FastAPI
from loguru import logger
from src.config import config
from src.utils import get_bot, client
from src.models import GroupMeCallback, Commands
from src.constants import Greetings, FailureReasons
from src.commands.help import help_msg
from src.commands.quote import get_quote
from src.commands.chart import create_chart
from src.commands.news import get_news
from src.commands.monte_carlo import monte_carlo
from src.commands.stats import calc_stats

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
            return {"status": "no message text"}

        time.sleep(2)

        try:
            if msg == Commands.HELP.value.command:
                logger.debug("calling help_msg")
                help_msg(bot)

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

            elif msg_split[0] == Commands.STATS.value.command:
                logger.debug("calling stats")
                calc_stats(msg, bot)

        except Exception as e:
            logger.exception(e)
            # bot.post(e)
            bot.post(
                f"Sorry about that, {random.choice(list(Greetings)).value}. {random.choice(list(FailureReasons)).value}"
            )
            return {"status": "error"}

    return {"status": "success"}

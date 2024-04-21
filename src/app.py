import re
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from src.config import config
from src.utils import bot
from src.models import GroupMeCallback, Commands
from src.constants import Greetings, FailureReasons
from src.commands.help import help_msg
from src.commands.quote import get_quote
from src.commands.chart import create_chart
from src.commands.news import get_news
from src.commands.monte_carlo import monte_carlo
from src.commands.stats import calc_stats
from src.commands.portfolio_opt import portfolio_opt
from src.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield

app = FastAPI(
    title=bot.name,
    summary="GroupMe bot to keep you up to date on finance.",
    version=config.version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/financialadvisors")
async def financialadvisors(request: GroupMeCallback):
    logger.info(f"{request=}")

    if request.sender_type != "bot":
        msg = request.text
        msg_split = msg.split()

        if msg == "":
            return {"status": "no message text"}

        try:
            if msg == Commands.HELP.value.command:
                logger.debug("calling help_msg")
                help_msg()

            elif len(re.findall(r"\$\^?[a-zA-Z.]+", msg)) > 0:
                logger.debug("calling get_quote")
                get_quote(msg)

            elif msg_split[0] == Commands.CHART.value.command:
                logger.debug("calling create_chart")
                create_chart(msg)

            elif msg.lower().find("warren buffett") > -1:
                logger.debug("calling warren")
                bot.post('"Buy the fucking dip" - Warren Buffett')
                logger.debug("bot posted warren")

            elif msg.lower().find("crypto check") > -1:
                logger.debug("calling crypto check")
                get_quote("$BTC-USD $ETH-USD $LTC-USD $DOGE-USD")

            elif msg_split[0] == Commands.NEWS.value.command:
                logger.debug("calling get_news")
                get_news(msg)

            elif msg_split[0] == Commands.MC.value.command:
                logger.debug("calling monte_carlo")
                monte_carlo(msg)

            elif msg_split[0] == Commands.STATS.value.command:
                logger.debug("calling stats")
                calc_stats(msg)

            elif msg_split[0] == Commands.PO.value.command:
                logger.debug("calling port opt")
                portfolio_opt(msg)

        except Exception as e:
            logger.exception(e)
            # bot.post(e)
            bot.post(
                f"Sorry about that, {random.choice(list(Greetings)).value}. {random.choice(list(FailureReasons)).value}"
            )
            return {"status": "error"}

    return {"status": "success"}

import os
from datetime import date, timedelta
from loguru import logger
import yfinance as yf
import matplotlib.pyplot as plt
from groupy.api.attachments import Images
from pydantic import BaseModel, ValidationError
from src.config import config
from src.models import Commands
from src.constants import Intervals


class ChartModel(BaseModel):
    ticker: str
    period: int = 1
    interval: Intervals = Intervals.YEAR


def create_chart(msg, bot, client):
    logger.debug("inside create_chart")
    msg_split = msg.split()

    try:
        model = ChartModel(
            ticker=msg_split[1],
            period=msg_split[2],
            interval=msg_split[3],
        )
        logger.info(f"{model=}")
    except ValidationError as error:
        logger.error(error)
        bot.post(Commands.CHART.value.usage)
        return

    logger.debug(f"{model.period=}")
    if model.interval == Intervals.DAY:
        start_date = str(date.today() - timedelta(days=model.period))
        if model.period == 1:
            str_interval = "day"
        else:
            str_interval = "days"
    elif model.interval == Intervals.MONTH:
        start_date = str(date.today() - timedelta(months=model.period))
        if model.period == 1:
            str_interval = "month"
        else:
            str_interval = "months"
    elif model.interval == Intervals.YEAR:
        start_date = str(date.today() - timedelta(years=model.period))
        if model.period == 1:
            str_interval = "year"
        else:
            str_interval = "years"
    else:
        bot.post(Commands.CHART.value.usage)
        return
    logger.debug(f"start_date: {start_date}")

    data = yf.download(model.ticker, start=start_date)
    yf_ticker = yf.Ticker(model.ticker).info
    try:
        ticker_name = yf_ticker["shortName"]
    except KeyError as excp:
        logger.error(excp)
        ticker_name = model.ticker
    except Exception as excp:
        logger.error(excp)
        ticker_name = model.ticker

    replymsg = f'{ticker_name}\nDollar Change: {round(data["Adj Close"][-1] - data["Adj Close"][0], 2)}\nPercent Change: {round(((data["Adj Close"][-1] / data["Adj Close"][0])-1)*100, 2)}%'

    data["Adj Close"].plot(
        title=f"{msg_split[1].upper()}, {model.period} {str_interval}"
    ).get_figure().savefig("tmp.png")
    logger.debug("chart created")
    bot.post(
        text=replymsg,
        attachments=[Images(client.session).from_file(open("tmp.png", "rb"))],
    )
    logger.info("bot posted chart")
    os.remove("tmp.png")
    plt.clf()
    logger.debug("chart removed")

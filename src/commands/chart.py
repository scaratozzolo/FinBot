import os
from datetime import date, timedelta
from loguru import logger
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from groupy.api.attachments import Images
from pydantic import BaseModel, ValidationError
from src.models import Commands
from src.constants import Intervals
from src.utils import bot, client


class ChartModel(BaseModel):
    ticker: str
    period: int = 1
    interval: Intervals = Intervals.YEAR


def create_chart(msg):
    logger.debug("inside create_chart")
    msg_split = msg.split()

    try:
        # TODO append None to msg_split to get to len 4 will allow for default values
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
        start_date = str(date.today() - timedelta(weeks=model.period * 4))
        if model.period == 1:
            str_interval = "month"
        else:
            str_interval = "months"
    elif model.interval == Intervals.YEAR:
        start_date = str(date.today() - timedelta(weeks=model.period * 52))
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

    replymsg = f'{ticker_name}\nDollar Change: {round(data["Adj Close"].iloc[-1] - data["Adj Close"].iloc[0], 2)}\nPercent Change: {round(((data["Adj Close"].iloc[-1] / data["Adj Close"].iloc[0])-1)*100, 2)}%'

    mpf.plot(
        data,
        type="line",
        title=f"{msg_split[1].upper()}, {model.period} {str_interval}",
        savefig=dict(fname="tmp.png", dpi=100, pad_inches=0.25),
        volume=True,
        mav=(20, 50),
        style="yahoo",
        tight_layout=True,
    )
    logger.debug("chart created")
    bot.post(
        text=replymsg,
        attachments=[Images(client.session).from_file(open("tmp.png", "rb"))],
    )
    logger.info("bot posted chart")
    os.remove("tmp.png")
    plt.clf()
    logger.debug("chart removed")

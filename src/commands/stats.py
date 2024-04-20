import os
from datetime import date, timedelta
from src.constants import Intervals
from src.models import Commands
from pydantic import BaseModel, ValidationError
import yfinance as yf
import matplotlib.pyplot as plt
from groupy.api.attachments import Images
from loguru import logger

class StatsModel(BaseModel):

    ticker: str
    period: int
    interval: Intervals


def calc_stats(msg, bot, client):

    msg_split = msg.split()

    try:
        model = StatsModel(
            ticker=msg_split[1],
            period=msg_split[2],
            interval=msg_split[3],
        )
        logger.info(f"{model=}")
    except ValidationError as error:
        logger.error(error)
        bot.post(Commands.CHART.value.usage)
        return

    if msg_split[-1] == Intervals.DAY.value:
        start_date = str(date.today() - timedelta(days=model.period))
        if model.period == 1:
            str_interval = "day"
        else:
            str_interval = "days"
    elif msg_split[-1] == Intervals.MONTH.value:
        start_date = str(date.today() - timedelta(months=model.period))
        if model.period == 1:
            str_interval = "month"
        else:
            str_interval = "months"
    elif msg_split[-1] == Intervals.YEAR.value:
        start_date = str(date.today() - timedelta(years=model.period))
        if model.period == 1:
            str_interval = "year"
        else:
            str_interval = "years"
    else:
        bot.post(Commands.STATS.value.usage)
        return None
    
    logger.debug(f"{start_date=}")

    data = yf.download(model.ticker, start=start_date)
    logger.debug(f"{len(data)=}")

    returns = data['Adj Close'].pct_change()*100
    mean = round(returns.mean(), 2)
    vol = round(returns.std(), 2)
    var95 = round(returns.quantile(0.05), 2)
    cvar95 = round(returns[returns.lt(var95)].mean(), 2)
    logger.debug("stats calculated")

    replymsg = f"{model.ticker} Historical Statistics\nMean: {mean}%\nVol: {vol}%\nVaR 95%: {var95}%\nCVaR 95: {cvar95}%"

    returns.hist()
    plt.title(f"{model.ticker} Returns Distribution, {model.period} {str_interval}")
    plt.savefig("tmp.png")
    bot.post(text=replymsg, attachments=[Images(client.session).from_file(open("tmp.png", "rb"))])
    logger.debug("message sent")
    os.remove("tmp.png")
    plt.clf()
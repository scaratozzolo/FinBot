import os
from datetime import date, timedelta
import numpy as np
import pandas as pd
import yfinance as yf
from groupy.api.attachments import Images
from scipy.stats import norm
from pydantic import BaseModel
from loguru import logger
import matplotlib.pyplot as plt
from src.constants import Intervals
from src.models import Commands


class MonteCarloModel(BaseModel):
    ticker: str
    period: int
    interval: Intervals


def monte_carlo(msg, bot, client):
    msg_split = msg.split()
    try:
        model = MonteCarloModel(
            ticker=msg_split[1].upper(), period=msg_split[2], interval=msg_split[3]
        )
        logger.debug(f"{model=}")
    except Exception as excp:
        logger.error(excp)
        bot.post(Commands.MC.value.usage)
        return

    if model.interval == Intervals.DAY.value:
        start_date = str(date.today() - timedelta(days=model.period))
        if model.period == 1:
            str_interval = "day"
        else:
            str_interval = "days"
    elif model.interval == Intervals.MONTH.value:
        start_date = str(date.today() - timedelta(months=model.period))
        if model.period == 1:
            str_interval = "month"
        else:
            str_interval = "months"
    elif model.interval == Intervals.YEAR.value:
        start_date = str(date.today() - timedelta(years=model.period))
        if model.period == 1:
            str_interval = "year"
        else:
            str_interval = "years"
    else:
        bot.post(Commands.MC.value.usage)
        return None

    bot.post("Calculating Monte Carlo Simulation...")

    iterations = 10000
    t_intervals = 252

    data = pd.DataFrame()
    data[model.ticker] = yf.download(model.ticker, start=start_date)["Adj Close"]

    log_returns = np.log(1 + data.pct_change())
    u = log_returns.mean()
    var = log_returns.var()
    stdev = log_returns.std()

    drift = u - (0.5 * var)

    daily_returns = np.exp(
        drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations))
    )

    S0 = data.iloc[-1]
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0
    for t in range(1, t_intervals):
        price_list[t] = price_list[t - 1] * daily_returns[t]

    final_prices = price_list[-1]
    returns = np.array(sorted(((price_list[-1] / price_list[0]) - 1) * 100))
    mean = round(final_prices.mean(), 2)
    var95 = round(returns[int(len(returns) * 0.05)], 2)
    cvar95 = round(returns[returns <= var95].mean(), 2)
    high = round(max(final_prices), 2)
    low = round(min(final_prices), 2)

    # replymsg = f"{yf.Ticker(ticker).info['shortName']} Monte Carlo Stats\n"\
    #            f"Sim. Price: ${mean}\nSim. VaR 95%: {var95}%\nSim. CVaR 95: {cvar95}%\nHigh: ${high}\nLow: ${low}"

    replymsg = f"{model.ticker} Monte Carlo Stats\nSim. Price: ${mean}\nSim. VaR 95%: {var95}%\nSim. CVaR 95: {cvar95}%\nHigh: ${high}\nLow: ${low}"

    plt.plot(price_list)
    plt.title(
        f"{model.ticker} Monte Carlo Simulation, Lookback: {model.period} {str_interval}, Lookahead: {t_intervals}"
    )
    plt.savefig("tmp.png")
    bot.post(
        text=replymsg,
        attachments=[Images(client.session).from_file(open("tmp.png", "rb"))],
    )
    os.remove("tmp.png")
    plt.clf()

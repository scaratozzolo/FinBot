from config import *
__version__ = "1.4.2"

import os
import re
import time
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from flask import Flask, request

import pandas as pd
import numpy as np
from scipy.stats import norm
import pandas_datareader as pdr
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt

from PortfolioOpt import PortfolioOpt

import finnhub
import alpaca_trade_api as tradeapi


from groupy.client import Client
from groupy.api.bots import Bots
from groupy.api.attachments import Images
client = Client.from_token(groupme_access_token)




bot_manger = Bots(client.session)
bot = None
for i in bot_manger.list():
    if i.name == botname:
        bot = i
        break
if bot is None:
    bot = bot_manger.create(botname, group_id=group_id, callback_url=callback_url)

group_name = None
groups = list(client.groups.list_all())
for group in groups:
    if group.id == group_id:
        group_name = group.name
        break


fh_client = finnhub.Client(api_key=finnhub_api_key)
alpaca_api = tradeapi.REST(alpaca_api_key, alpaca_api_secret_key, base_url='https://paper-api.alpaca.markets')



app = Flask(__name__)

@app.route('/')
def index():
    return "Nothing to see here"

@app.route('/financialadvisors', methods=['POST'])
def financialadvisors():

    data = request.get_json()
    if data['name'] != bot.name:
        msg = data['text']
        msg_split = msg.split()

        time.sleep(2)

        # try:
        if msg == f"{bot_char}help":
            help_msg()

        elif len(re.findall(r"\$[a-zA-Z.]+", msg)) > 0:
            get_quote(msg)

        elif msg_split[0] == f"{bot_char}chart":
            create_chart(msg)

        elif msg_split[0] == f"{bot_char}po":
            portfolio_opt(msg)

        elif msg_split[0] == f"{bot_char}stats":
            calc_stats(msg)

        elif msg_split[0] == f"{bot_char}mc":
            monte_carlo(msg)

        elif msg_split[0] == f"{bot_char}news":
            get_news(msg)

        elif msg_split[0] == f"{bot_char}portfolio":
            manage_portfolio(msg)


        # except Exception as e:
        #     print(e)
        #     # bot.post(e)
        #     bot.post("Something went wrong. Make sure you entered the command correctly, otherwise the function is broken.")

    return "success"



def help_msg():

    replymsg = f"FinBot v{__version__} Help\n"
    replymsg += "1. $<ticker> will reply with a live quote of the ticker, example $TSLA\n"
    replymsg += f"2. {bot_char}chart will return a chart of a given ticker\n"
    replymsg += f"3. {bot_char}po will return opimal weights for a given portfolio\n"
    replymsg += f"4. {bot_char}stats will calculate daily historical statistics over a given time range\n"
    replymsg += f"5. {bot_char}mc will run a Monte Carlo simulation based on data of a give time range\n"
    replymsg += f"6. {bot_char}news will return the latest new articles for the market or a specific ticker (default is 3)\n"
    replymsg += f"7. {bot_char}portfolio allows you to interact with the groupchat paper trading account\n"

    
    bot.post(replymsg)



def get_quote(msg):

    tickers = re.findall(r"\$[a-zA-Z.]+", msg)
    tickers = [ticker[1:].upper() for ticker in tickers]

    data = yf.download(tickers, start=date.today()-timedelta(days=1))["Adj Close"]
    quote = data.iloc[-1]
    pchange = (data.pct_change().dropna().iloc[0]*100).round(2)
    dchange = (data.iloc[-1] - data.iloc[0]).round(2)

    for ticker in tickers:
        try:

            replymsg = f"{yf.Ticker(ticker).info['shortName']} Quote:\nPrice: ${quote[ticker]}\nDollar Change: {dchange[ticker]}\n% Change: {pchange[ticker]}%"
            bot.post(replymsg)



        except Exception as e:
            print(e)




def create_chart(msg):

    msg_split = msg.split()
    if len(msg_split) != 4:
        bot.post(f"Usage: {bot_char}chart ticker period interval\nExample: {bot_char}chart TSLA 3 m\nAvailable intervals: d, m, y")
    else:
        period = int(msg_split[-2])
        if msg_split[-1] == "d":
            start_date = str(date.today() - relativedelta(days=period))
            if period == 1:
                interval = "day"
            else:
                interval = "days"
        elif msg_split[-1] == "m":
            start_date = str(date.today() - relativedelta(months=period))
            if period == 1:
                interval = "month"
            else:
                interval = "months"
        elif msg_split[-1] == "y":
            start_date = str(date.today() - relativedelta(years=period))
            if period == 1:
                interval = "year"
            else:
                interval = "years"
        else:
            bot.post(f"Usage: {bot_char}chart ticker period interval\nExample: {bot_char}chart TSLA 3 m\nAvailable intervals: d, m, y")
            return None

        data = pdr.get_data_yahoo(msg_split[1], start=start_date)

        replymsg = f'{yf.Ticker(msg_split[1].upper()).info["shortName"]}\nDollar Change: {round(data["Adj Close"][-1] - data["Adj Close"][0], 2)}\nPercent Change: {round(((data["Adj Close"][-1] / data["Adj Close"][0])-1)*100, 2)}%'

        data["Adj Close"].plot(title=f"{msg_split[1].upper()}, {period} {interval}").get_figure().savefig("tmp.png")
        bot.post(text=replymsg, attachments=[Images(client.session).from_file(open("tmp.png", "rb"))])
        os.remove("tmp.png")
        plt.clf()


def portfolio_opt(msg):

    msg_split = msg.split()
    if len(msg_split) == 1:
        bot.post(f"Usage: {bot_char}po period interval opt_for comma, seperated, tickers\nExample: {bot_char}po 3 y sharpe DIS, TSLA, GOOG\nAvailable intervals: d, m, y\nAvailable optimizations: sharpe, returns, vol\nPeriod and interval is the length of the lookback data")
    else:

        if msg_split[2] == "d":
            start_date = str(date.today() - relativedelta(days=int(msg_split[1])))
        elif msg_split[2] == "m":
            start_date = str(date.today() - relativedelta(months=int(msg_split[1])))
        elif msg_split[2] == "y":
            start_date = str(date.today() - relativedelta(years=int(msg_split[1])))
        else:
            bot.post(f"Usage: {bot_char}po period interval opt_for comma, seperated, tickers\nExample: {bot_char}po 3 y sharpe DIS, TSLA, GOOG\nAvailable intervals: d, m, y\nAvailable optimizations: sharpe, returns, vol\nPeriod and interval is the length of the lookback data")
            return None

        tickers = [i.replace(" ", "").replace(",", "").upper() for i in msg_split[4:]]
        opt = PortfolioOpt(tickers, start=start_date)
        weights = opt.optimize_portfolio(opt_for=msg_split[3], print_results=False)['x']

        if msg_split[3] == "sharpe":
            opt_for = "Maximum Sharpe"
        elif msg_split[3] == "returns":
            opt_for = "Maximum Returns"
        elif msg_split[3] == "vol":
            opt_for = "Minimum Volatility"
        else:
            bot.post(f"Usage: {bot_char}po period interval opt_for comma, seperated, tickers\nExample: {bot_char}po 3 y sharpe DIS, TSLA, GOOG\nAvailable intervals: d, m, y\nAvailable optimizations: sharpe, returns, vol\nPeriod and interval is the length of the lookback data")
            return None

        replymsg = f"Optimal Weights for {opt_for}:\n"

        for tick, weight in zip(tickers, weights):
            if round(weight*100, 2) > 0:
                replymsg += f"{tick}: {round(weight*100, 2)}%\n"

        bot.post(replymsg)



def calc_stats(msg):

    msg_split = msg.split()
    if len(msg_split) != 4:
        bot.post(f"Usage: {bot_char}stats ticker period interval\nExample: {bot_char}stats AAPL 3 y\nAvailable intervals: d, m, y")
    else:
        period = int(msg_split[-2])
        if msg_split[-1] == "d":
            start_date = str(date.today() - relativedelta(days=period))
            if period == 1:
                interval = "day"
            else:
                interval = "days"
        elif msg_split[-1] == "m":
            start_date = str(date.today() - relativedelta(months=period))
            if period == 1:
                interval = "month"
            else:
                interval = "months"
        elif msg_split[-1] == "y":
            start_date = str(date.today() - relativedelta(years=period))
            if period == 1:
                interval = "year"
            else:
                interval = "years"
        else:
            bot.post(f"Usage: {bot_char}stats ticker period interval\nExample: {bot_char}stats AAPL 3 y\nAvailable intervals: d, m, y")
            return None

        ticker = msg_split[1].upper()
        data = pdr.get_data_yahoo(ticker, start=start_date)

        returns = data['Adj Close'].pct_change()*100
        mean = round(returns.mean(), 2)
        vol = round(returns.std(), 2)
        var95 = round(returns.quantile(0.05), 2)
        cvar95 = round(returns[returns.lt(var95)].mean(), 2)

        replymsg = f"{yf.Ticker(ticker).info['shortName']} Historical Statistics\n"\
                   f"Mean: {mean}%\nVol: {vol}%\nVaR 95%: {var95}%\nCVaR 95: {cvar95}%"

        returns.hist()
        plt.title(f"{ticker} Returns Distribution, {period} {interval}")
        plt.savefig("tmp.png")
        bot.post(text=replymsg, attachments=[Images(client.session).from_file(open("tmp.png", "rb"))])
        os.remove("tmp.png")
        plt.clf()



def monte_carlo(msg):

    msg_split = msg.split()
    if len(msg_split) != 4:
        bot.post(f"Usage: {bot_char}mc ticker period interval\nExample: {bot_char}mc AAPL 3 y\nAvailable intervals: d, m, y")
    else:
        period = int(msg_split[-2])
        if msg_split[-1] == "d":
            start_date = str(date.today() - relativedelta(days=period))
            if period == 1:
                interval = "day"
            else:
                interval = "days"
        elif msg_split[-1] == "m":
            start_date = str(date.today() - relativedelta(months=period))
            if period == 1:
                interval = "month"
            else:
                interval = "months"
        elif msg_split[-1] == "y":
            start_date = str(date.today() - relativedelta(years=period))
            if period == 1:
                interval = "year"
            else:
                interval = "years"
        else:
            bot.post(f"Usage: {bot_char}mc ticker period interval\nExample: {bot_char}mc AAPL 3 y\nAvailable intervals: d, m, y")
            return None


        iterations=10000
        t_intervals=252

        ticker = msg_split[1].upper()
        data = pd.DataFrame()
        data[ticker] = pdr.get_data_yahoo(ticker, start=start_date)['Adj Close']

        log_returns = np.log(1 + data.pct_change())
        u = log_returns.mean()
        var = log_returns.var()
        stdev = log_returns.std()

        drift = u - (0.5 * var)

        daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(t_intervals, iterations)))

        S0 = data.iloc[-1]
        price_list = np.zeros_like(daily_returns)
        price_list[0] = S0
        for t in range(1, t_intervals):
            price_list[t] = price_list[t - 1] * daily_returns[t]

        final_prices = price_list[-1]
        returns = np.array(sorted(((price_list[-1]/price_list[0]) - 1)*100))
        mean = round(final_prices.mean(), 2)
        var95 = round(returns[int(len(returns) * 0.05)], 2)
        cvar95 = round(returns[returns <= var95].mean(), 2)
        high = round(max(final_prices), 2)
        low = round(min(final_prices), 2)

        replymsg = f"{yf.Ticker(ticker).info['shortName']} Monte Carlo Stats\n"\
                   f"Sim. Price: ${mean}\nSim. VaR 95%: {var95}%\nSim. CVaR 95: {cvar95}%\nHigh: ${high}\nLow: ${low}"

        plt.plot(price_list)
        plt.title(f"{ticker} Monte Carlo Simulation, Lookback: {period} {interval}, Lookahead: {t_intervals}")
        plt.savefig("tmp.png")
        bot.post(text=replymsg, attachments=[Images(client.session).from_file(open("tmp.png", "rb"))])
        os.remove("tmp.png")
        plt.clf()



def get_news(msg):

    msg_split = msg.split()
    if len(msg_split) > 3:
        bot.post(f"Usage: {bot_char}news <ticker> num_articles\nExample: {bot_char}news 5\nExample: {bot_char}news AAPL 10\n")
    else:

        default_articles = 3

        if len(msg_split) == 1:
            num_articles = default_articles
            ticker = None
        elif len(msg_split) == 2:
            try:
                num_articles = int(msg_split[1])
                ticker = None
            except:
                num_articles = default_articles
                ticker = msg_split[1]
        else:
            num_articles = int(msg_split[2])
            ticker = msg_split[1]


        if ticker is not None:
            res = fh_client.company_news(ticker, _from=str(date.today()), to=str(date.today()))
        else:
            res = fh_client.general_news("general")

        bot.post(f"Total articles found: {len(res)}")

        for i in res[:num_articles]:
            
            replymsg = f"Headline: {i['headline']}\n\nSummary: {i['summary']}\n\n{i['url']}"

            bot.post(replymsg)


def manage_portfolio(msg):

    msg_split = msg.split()

    available_commands = ["buy", "sell"] # history

    if len(msg_split) == 1:
        account = alpaca_api.get_account()

        replymsg = ""

        replymsg += f"{group_name}\n"
        replymsg += f"Value: ${float(account.equity)}\n\n"
        replymsg += f"Buying Power: ${float(account.buying_power)}\nCash: ${float(account.cash)}\n\n"
        replymsg += f"Dollar Change: {round(float(account.equity)-float(account.last_equity), 2)}\nPercent Change: {round(((float(account.equity)/float(account.last_equity))-1)*100, 2)}%\n\n"

        replymsg += "Postions:\n"
        positions = alpaca_api.list_positions()
        for pos in positions:
            replymsg += f"{pos.symbol}: {pos.side.upper()} {pos.qty} @ ${pos.avg_entry_price}\n"
            replymsg += f"Market Value: ${pos.market_value}\n"
            replymsg += f"P/L Today: {pos.unrealized_intraday_pl}, {round(float(pos.unrealized_intraday_plpc)*100, 2)}%\n"
            replymsg += f"P/L Open: {pos.unrealized_pl}, {round(float(pos.unrealized_plpc)*100, 2)}%\n\n"

        bot.post(replymsg)

    elif msg_split[1] in available_commands:
        

        if msg_split[1] == "buy" or msg_split[1] == "sell":
            if len(msg_split) == 2:
                bot.post(f"Usage: {bot_char}portfolio buy/sell ticker shares\nExample: {bot_char}portfolio buy AAPL 10\nExample: {bot_char}portfolio sell TSLA 10")
            else:
                res = alpaca_api.submit_order(
                    symbol=msg_split[2].upper(),
                    side=msg_split[1] ,
                    type='market',
                    qty=msg_split[3],
                    time_in_force='day',
                )

                bot.post(f"Order ID: {res.id}\nOrder Status: {res.status}")

    else:
        bot.post(f"Usage: {bot_char}portfolio WIP\nExample: {bot_char}portfolio")

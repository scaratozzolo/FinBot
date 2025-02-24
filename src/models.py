from enum import Enum
from pydantic import BaseModel
from src.config import config
from src.constants import Intervals
from src.utils import bot


class GroupMeCallback(BaseModel):
    attachments: list = []
    avatar_url: str = ""
    created_at: int = 0
    group_id: str = ""
    id: str = ""
    name: str
    sender_id: str = ""
    sender_type: str = ""
    source_guid: str = ""
    system: bool = False
    text: str
    user_id: str = ""


class Command(BaseModel):
    command: str
    description: str
    usage: str


class Commands(Enum):
    HELP = Command(
        command=f"{config.bot_char}help",
        description="Gives an overview of the available commands.",
        usage="help",
    )

    QUOTE = Command(
        command="",
        description=f"By adding a $ to a ticker, {bot.name} will return a live quote for the ticker.",
        usage="$<ticker>\nExample: $AAPL $TSLA $BTC-USD",
    )

    NEWS = Command(
        command=f"{config.bot_char}news",
        description="Returns the latest new articles for the market or a specific ticker (default is 3).",
        usage=f"{config.bot_char}news <ticker> num_articles\nExample: {config.bot_char}news 5\nExample: {config.bot_char}news AAPL 10\n",
    )

    CHART = Command(
        command=f"{config.bot_char}chart",
        description="Returns a chart of a given ticker.",
        usage=f"{config.bot_char}chart ticker period interval\nExample: {config.bot_char}chart TSLA 3 m\nAvailable intervals: {', '.join(i.value for i in Intervals)}",
    )

    PO = Command(
        command=f"{config.bot_char}po",
        description="Returns opimal weights for a given portfolio.",
        usage=f"{config.bot_char}po period interval opt_for comma, seperated, tickers\nExample: {config.bot_char}po 3 y sharpe DIS, TSLA, GOOG\nAvailable intervals: {', '.join(i.value for i in Intervals)}.\nAvailable optimizations: sharpe, returns, vol.\nPeriod and interval is the length of the lookback data.",
    )

    MC = Command(
        command=f"{config.bot_char}mc",
        description="Runs a Monte Carlo simulation based on data of a give time range.",
        usage=f"{config.bot_char}mc ticker period interval\nExample: {config.bot_char}mc AAPL 3 y\nAvailable intervals: {', '.join(i.value for i in Intervals)}.",
    )

    STATS = Command(
        command=f"{config.bot_char}stats",
        description="Calculates daily historical statistics over a given time range.",
        usage=f"{config.bot_char}stats ticker period interval\nExample: {config.bot_char}stats AAPL 3 y\nAvailable intervals: {', '.join(i.value for i in Intervals)}.",
    )

    WATCHLIST = Command(
        command=f"{config.bot_char}watch",
        description="A watchlist of tickers for the group.",
        usage=f"{config.bot_char}watch ticker",
    )

    EARNINGS = Command(
        command=f"{config.bot_char}earnings",
        description="Retuns earnings dates for tickers in watchlist for the next 7 days.",
        usage=f"{config.bot_char}earnings",
    )

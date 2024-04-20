import typing
from enum import Enum
from pydantic import BaseModel
from src.config import config
from src.commands.help import help_msg


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


class Intervals(Enum):
    DAY = "d"
    MONTH = "m"
    YEAR = "y"
    # YEAR_TO_DATE = "ytd"


class Command(BaseModel):
    command: str
    description: str
    usage: str
    func: typing.Callable


class Commands(Enum):
    HELP = Command(
        command=f"{config.bot_char}help",
        description="Gives an overview of the available commands.",
        usage="help",
        func=help_msg,
    )

    QUOTE = Command(
        command="",
        description=f"By adding a $ to a ticker, {config.botname} will return a live quote for the ticker.",
        usage="$<ticker>\nExample: $AAPL $TSLA $BTC-USD",
        func=lambda x: "WIP",
    )

    CHART = Command(
        command=f"{config.bot_char}chart",
        description="Returns a chart of a given ticker.",
        usage=f"{config.bot_char}chart ticker period interval\nExample: {config.bot_char}chart TSLA 3 m\nAvailable intervals: {', '.join(i.value for i in Intervals)}",
        func=lambda x: "WIP",
    )

    PO = Command(
        command=f"{config.bot_char}po",
        description="Returns opimal weights for a given portfolio",
        usage=f"{config.bot_char}po period interval opt_for comma, seperated, tickers",
        func=lambda x: "WIP",
    )

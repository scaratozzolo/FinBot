from enum import Enum


class Intervals(Enum):
    DAY = "d"
    MONTH = "m"
    YEAR = "y"
    # YEAR_TO_DATE = "ytd"

class OptimizeFor(Enum):

    SHARPE = "sharpe"
    RETURNS = "returns"
    VOLATILITY = "vol"

class Greetings(Enum):

    CHIEF = "Chief"
    POP = "Pop"
    BEASTO = "Beasto"
    KING = "King"
    SIR = "Sir"

class FailureReasons(Enum):

    ONE = "Something went wrong."
    TWO = "It appears there's been a problem."
    THREE = "Just not feeling it right now."
    FOUR = "I don't like your vibe."
    FIVE = "Maybe try again?"

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
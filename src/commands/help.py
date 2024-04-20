from loguru import logger
from src.config import config
from src.models import Commands
from src.utils import bot


def help_msg() -> str:
    logger.debug("inside help_msg")

    bot.post(f"{bot.name} v{config.version} Help")

    for i, command in enumerate(Commands):
        logger.debug(f"{command=}")
        value = command.value.command
        bot.post(
            f"{i+1}. {value if value else ''}{' - ' if value else ''}{command.value.description}\nUsage: {command.value.usage}"
        )

    bot.post("Follow along on GitHub: https://github.com/scaratozzolo/FinBot")
    logger.debug("bot posted help")

from loguru import logger
from src.config import config
from src.models import Commands


def help_msg(bot) -> str:
    logger.debug("inside help_msg")

    replymsg = f"{config.botname} v{config.version} Help\n"

    for i, command in enumerate(Commands):
        logger.debug(f"{command=}")
        value = command.value.command
        replymsg += f"{i+1}. {value if value else ''}{' - ' if value else ''}{command.value.description}\n{command.value.usage}\n\n"

    replymsg += f"Follow along on GitHub: https://github.com/scaratozzolo/FinBot"

    bot.post(replymsg)
    logger.debug("bot posted help")

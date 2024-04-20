from loguru import logger
from src.config import config


def help_msg(bot, commands) -> str:

    logger.debug("inside help_msg")

    replymsg = f"{config.botname} v{config.version} Help\n"

    for i, command in enumerate(commands):
        logger.debug(f"{command=}")
        value = command.value.command
        replymsg += f"{i+1}. {value if value else ''}{' - ' if value else ''}{command.value.description}\n{command.value.usage}\n\n"

    replymsg += f"Follow along on GitHub: https://github.com/scaratozzolo/FinBot"

    # bot.post(replymsg)
    print(replymsg)
    logger.debug("bot posted help")
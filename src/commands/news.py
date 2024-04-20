from datetime import date
from loguru import logger
from src.config import config
from src.utils import get_finnhub_client
from src.models import Commands

fh_client = get_finnhub_client()

def get_news(msg, bot):

    msg_split = msg.split()
    if len(msg_split) > 3:
        bot.post(Commands.NEWS.value.usage)
    else:

        default_articles = 3

        if len(msg_split) == 1:
            num_articles = default_articles
            ticker = None
        elif len(msg_split) == 2:
            try:
                num_articles = int(msg_split[1])
                ticker = None
            except Exception as excp:
                logger.error(excp)
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
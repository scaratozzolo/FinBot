import typing
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    version: str = "2.1.0"

    request_token: str

    groupme_access_token: str

    bot_id: typing.Optional[str] = None
    bot_char: str = "?"

    group_id: typing.Optional[str] = None
    botname: typing.Optional[str] = None
    callback_url: typing.Optional[str] = None

    av_api_key: str
    finnhub_api_key: str

    alpaca_api_key: typing.Optional[str] = None
    alpaca_api_secret_key: typing.Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


config = Config()

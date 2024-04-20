import typing
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    version: str = "2.0.0b1"
    botname: str = "FinBot"
    bot_char: str = "?"

    groupme_access_token: str
    group_id: str

    callback_url: str

    av_api_key: str
    finnhub_api_key: str

    alpaca_api_key: typing.Optional[str] = None
    alpaca_api_secret_key: typing.Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


config = Config()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    bot_token_test: SecretStr
    mega_email: SecretStr
    mega_password: SecretStr
    ue_land_group: SecretStr
    me_pm: SecretStr
    training_ground: SecretStr
    db_url: SecretStr

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()

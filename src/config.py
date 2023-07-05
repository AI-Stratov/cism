import os

from pydantic import BaseSettings, PositiveInt


class AppSettings(BaseSettings):
    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/../.env"
        env_file_encoding = "utf-8"

    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: PositiveInt = 5432
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE: int = 30

    @property
    def sql_alchemy_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = AppSettings()

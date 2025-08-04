# app/core/config.py
import pydantic.v1
from pydantic import Field

class Settings(pydantic.v1.BaseSettings):
    DB_HOST: str = Field(...)
    DB_PORT: int = Field(...)
    DB_USER: str = Field(...)
    DB_PASSWORD: str = Field(...)
    DB_NAME: str = Field(...)

    SECRET_KEY: str = Field(...)

    AWS_ACCESS_KEY_ID: str = Field(...)
    AWS_SECRET_ACCESS_KEY: str = Field(...)
    AWS_DEFAULT_REGION: str = Field(...)
    S3_BUCKET_NAME: str = Field(...)

    REDIS_HOST: str = Field(...)
    REDIS_PORT: int = Field(...)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings(

)

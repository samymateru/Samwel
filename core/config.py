from typing import Optional
import pydantic.v1
from pydantic import Field

class Settings(pydantic.v1.BaseSettings):
    DB_HOST: Optional[str] = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_NAME: str = Field(default="postgres")

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


settings = Settings()

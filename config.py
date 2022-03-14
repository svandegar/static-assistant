import os
from typing import List

from pydantic import BaseSettings

allowed_sources = os.getenv("allowed_host_sources", "*").split(',')


class Settings(BaseSettings):
    POSTMARK_TOKEN: str
    default_from_email: str
    default_recipient_email: str
    subject_prefix: str = "Nouveau message :"
    allowed_host_sources: List[str] = allowed_sources

    class Config:
        env_file = ".env"


settings = Settings()

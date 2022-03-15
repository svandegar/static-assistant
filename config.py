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
    blocked_emails: List[str] = ["spammer@email.be"]
    blocked_phrases: List[str] = ["please check this obscure website"]

    class Config:
        env_file = ".env"


settings = Settings()

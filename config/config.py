import json
from typing import List

from pydantic import BaseSettings

with open('./config/config.json', 'r') as config_file:
    config_data = json.load(config_file)


class Settings(BaseSettings):
    POSTMARK_TOKEN: str
    subject_prefix: str = "Nouveau message :"
    allowed_host_sources: List[str] = config_data.get("allowed_sources",["*"])
    blocked_emails: List[str] = config_data.get("spam", {}).get("emails", [])
    blocked_content: List[str] = config_data.get("spam", {}).get("content", [])
    default_from_email: str = config_data.get("email", {}).get("from")
    allow_default_recipient_email: str = config_data.get("email", {}).get("allow_default_to")
    recipients_emails: dict = config_data.get("email", {}).get("to")
    success_redirect_url: str = config_data.get("success_redirect_url", {})

    class Config:
        env_file = "config/.env"


settings = Settings()

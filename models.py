from pydantic import BaseModel


class Message(BaseModel):
    reply_to: str
    subject: str
    body: str
    full_name: str | None = None

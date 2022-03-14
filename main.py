from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

import config
from config import settings
from services import email
import models

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=config.settings.allowed_host_sources
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/contact")
async def post_contact(message: models.Message):
    subject = build_subject(subject=message.subject)
    html_body = build_body(body=message.body, subject=message.subject)
    email.send_email(
        reply_to_email=message.reply_to,
        subject=subject,
        html_body=html_body
    )
    return {"message": f"Message sent"}


def build_subject(subject: str) -> str:
    return f"{settings.subject_prefix} {subject}"

def build_body(body: str, subject: str) -> str:
    return f"""
    <h1>{subject}</h1>
    <p>{body}</p>
    """

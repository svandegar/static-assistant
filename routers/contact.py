from fastapi import APIRouter, HTTPException, Request

from config.config import settings
from services import email
import models

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.post("")
async def post_contact(message: models.Message, request: Request):
    message_is_spam = detect_spam(message=message)
    if not message_is_spam:
        subject = build_subject(subject=message.subject)
        html_body = build_body(body=message.body, subject=message.subject)
        recipient_email = identify_recipient_email(host_name=request.client.host)
        email.send_email(
            reply_to_email=message.reply_to,
            recipient_email=recipient_email,
            subject=subject,
            html_body=html_body
        )
        return {"message": f"Message sent"}
    else:
        raise HTTPException(status_code=400, detail="Looks like spam.")


def build_subject(subject: str) -> str:
    return f"{settings.subject_prefix} {subject}"


def build_body(body: str, subject: str) -> str:
    return f"""
    <h1>{subject}</h1>
    <p>{body}</p>
    """


def detect_spam(message: models.Message) -> bool:
    if message.reply_to in settings.blocked_emails:
        return True

    if any([phrase.lower() in message.body.lower() for phrase in settings.blocked_content]):
        return True

    return False


def identify_recipient_email(host_name: str) -> str:
    """
    Returns the email address linked to the host issuing the request
    :param host: requester host name
    :return: recipient email
    """
    email = settings.recipients_emails.get(host_name)
    if email:
        return email
    else:
        if settings.allow_default_recipient_email:
            return settings.recipients_emails.get("default")
        else:
            raise HTTPException(status_code=400, detail="Unknown host")

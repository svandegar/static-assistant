from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, Form
from starlette.responses import RedirectResponse

from config.config import settings
from services import email
import models

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)


@router.post("")
async def post_contact(message: models.Message, request: Request):
    message_is_handled = handle_message(parsed_message=message, request=request)
    if message_is_handled:
        return {"message": f"Message sent"}
    else:
        raise HTTPException(status_code=400, detail="Looks like spam.")


@router.post("/form")
async def post_contact(request: Request,
                       # message: Annotated[str, Form(None)],
                       message: str = Form(""),
                       name: str = Form(...),
                       reply_to: str = Form(...),
                       subject: str = Form(...),
                       organization: str = Form(...)):
    parsed_message = models.Message(
        reply_to=reply_to,
        body=message,
        organization=organization,
        name=name,
        subject=subject
    )
    message_is_handled = handle_message(parsed_message=parsed_message, request=request)
    if message_is_handled:
        return RedirectResponse(url=(settings.success_redirect_url.get(request.client.host) or settings.success_redirect_url.get("default")), status_code=303)
    else:
        raise HTTPException(status_code=400, detail="Looks like spam.")


def build_subject(subject: str) -> str:
    return f"{settings.subject_prefix} {subject}"


def build_body(body: str, subject: str, name: str, organization: str) -> str:
    return f"""
    <div><b>Subject</b> : {subject}</div>
    <div><b>Name</b> : {name}</div>
    <div><b>Organization</b> : {organization}</div>
    <p>{body}</p>
    """


def detect_spam(message: models.Message) -> bool:
    if message.reply_to in settings.blocked_emails:
        return True

    if message.name in settings.blocked_names:
        return True

    if not any([phrase.lower() in message.subject.lower() for phrase in settings.allowed_subjects]):
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


def handle_message(parsed_message: models.Message, request: Request) -> bool:
    message_is_spam = detect_spam(message=parsed_message)
    if message_is_spam:
        return False
    else:
        subject = build_subject(subject=parsed_message.subject)
        html_body = build_body(
            body=parsed_message.body,
            subject=parsed_message.subject,
            organization=parsed_message.organization,
            name=parsed_message.name
        )
        recipient_email = identify_recipient_email(host_name=request.client.host)
        email.send_email(
            reply_to_email=parsed_message.reply_to,
            recipient_email=recipient_email,
            subject=subject,
            html_body=html_body
        )
        return True

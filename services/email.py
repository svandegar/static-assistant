from postmarker.core import PostmarkClient

from config.config import settings

POSTMARK_TOKEN = settings.POSTMARK_TOKEN
postmark_client = PostmarkClient(server_token=POSTMARK_TOKEN)


def send_email(subject: str,
               html_body: str,
               reply_to_email: str,
               from_email: str | None = None,
               recipient_email: str | None = None):
    result = postmark_client.emails.send(
        From=from_email or settings.default_from_email,
        To=recipient_email or settings.default_recipient_email,
        ReplyTo=reply_to_email,
        Subject=subject,
        HtmlBody=html_body
    )
    return result

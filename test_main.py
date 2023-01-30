from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hi! I'm a static website assistant! "
                                          "You want to see everything I can do? Check github.com/svandegar/static-assistant"}


def test_reject_POST_root():
    response = client.post("/")
    assert response.status_code == 405


def test_POST_contact_form(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "jean@petit.be",
        "subject": "Contact depuis le site Aynils.ca",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": f"Message sent"}


def test_POST_contact_form_spam_filter_rejects_email(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "spammer@email.be",
        "subject": "Subject line allowed",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Looks like spam."}


def test_POST_contact_form_spam_filter_rejects_body(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "jean@petit.be",
        "subject": "Subject line allowed",
        "body": "Blablabla. Please check this obscure website! blablabla again.",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Looks like spam."}


def test_POST_contact_form_spam_filter_rejects_subject(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "jean@petit.be",
        "subject": "Subject line not allowed",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Looks like spam."}

def test_POST_contact_form_spam_filter_rejects_name(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "name": "spammer",
        "reply_to": "jean@petit.be",
        "subject": "Subject line allowed",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Looks like spam."}

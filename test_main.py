from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from main import app

client = TestClient(app)
client.headers["Host"] = "https://testhost.com"


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_reject_POST_root():
    response = client.post("/")
    assert response.status_code == 405


def test_POST_contact_form(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "jean@petit.be",
        "subject": "Subject line",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": f"Message sent"}


def test_POST_contact_form_spam_filter_rejects_email(mocker: MockerFixture):
    mocker.patch('services.email.send_email')
    data = {
        "reply_to": "spammer@email.be",
        "subject": "Subject line",
        "body": "Here comes the body",
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail":"Looks like spam."}

import uuid

import pytest

import data
import sender_requests


@pytest.fixture
def login():
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"
    response = sender_requests.post_login(data.login_body)
    assert response.status_code == 200, response.text
    return response


@pytest.fixture
def cleanup():
    channel_ids = []

    def _register_channel(channel_id: str):
        if channel_id:
            channel_ids.append(channel_id)
        return channel_id

    yield _register_channel

    for channel_id in reversed(channel_ids):
        sender_requests.delete_channel(channel_id)


@pytest.fixture
def channel(login, cleanup):
    body = data.channel_body.copy()
    body["title"] = f"Autotest {uuid.uuid4()}"

    response = sender_requests.post_create_channel(body)
    assert response.status_code == 201, response.text

    channel_id = response.json()["channel_id"]
    cleanup(channel_id)
    return channel_id

import uuid
import sender_requests


def test_create_channel_duplicate_title(login, cleanup):
    title = f"Autotest channel {uuid.uuid4()}"
    body = {"title": title}

    first_response = sender_requests.post_create_channel(body)
    assert first_response.status_code == 201
    channel_id = first_response.json()["channel_id"]
    cleanup(channel_id)

    second_response = sender_requests.post_create_channel(body)
    assert second_response.status_code == 409

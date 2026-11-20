import uuid
import data
import sender_requests


def test_create_channel_success(login, cleanup):
    body = data.channel_body.copy()
    body["title"] = f"Autotest channel {uuid.uuid4()}"

    response = sender_requests.post_create_channel(body)
    assert response.status_code == 201

    result = response.json()
    assert "channel_id" in result
    assert isinstance(result["channel_id"], str)

    cleanup(result["channel_id"])

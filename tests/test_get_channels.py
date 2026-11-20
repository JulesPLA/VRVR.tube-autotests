import uuid
import sender_requests


def test_get_channels_contains_created_channel(login, cleanup):
    title = f"Autotest {uuid.uuid4()}"
    create_response = sender_requests.post_create_channel({"title": title})
    assert create_response.status_code == 201
    channel_id = create_response.json()["channel_id"]
    cleanup(channel_id)

    response = sender_requests.get_channels()
    assert response.status_code == 200

    channels = response.json()
    ids = [channel["id"] for channel in channels]
    assert channel_id in ids

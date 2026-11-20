import uuid
import sender_requests


def test_get_channel_by_id_success(login, cleanup):
    title = f"Autotest {uuid.uuid4()}"
    create_response = sender_requests.post_create_channel({"title": title})
    assert create_response.status_code == 201
    channel_id = create_response.json()["channel_id"]
    cleanup(channel_id)

    response = sender_requests.get_channel(channel_id)
    assert response.status_code == 200

    channel = response.json()
    assert channel["id"] == channel_id
    assert channel["title"] == title
    assert "is_free_play_mode" in channel
    assert "play_mode" in channel

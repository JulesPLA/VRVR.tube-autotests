import uuid
import sender_requests


def test_update_channel_title_success(channel):
    new_title = f"Updated {uuid.uuid4()}"
    update_response = sender_requests.put_update_channel(channel, {"title": new_title})
    assert update_response.status_code == 200, update_response.text

    get_response = sender_requests.get_channel(channel)
    assert get_response.status_code == 200

    result = get_response.json()
    assert result["title"] == new_title

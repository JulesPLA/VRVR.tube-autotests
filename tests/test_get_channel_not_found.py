import uuid
import sender_requests


def test_get_channel_not_found(login):
    fake_channel_id = str(uuid.uuid4())
    response = sender_requests.get_channel(fake_channel_id)
    assert response.status_code == 404

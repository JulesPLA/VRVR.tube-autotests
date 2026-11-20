import uuid
import sender_requests


def test_delete_non_existing_channel(login):
    fake_id = str(uuid.uuid4())
    response = sender_requests.delete_channel(fake_id)
    assert response.status_code == 404

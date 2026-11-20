import uuid
import sender_requests


def test_delete_folder_invalid_channel_id(login):
    fake_channel_id = str(uuid.uuid4())
    fake_folder_id = str(uuid.uuid4())
    response = sender_requests.delete_folder(fake_channel_id, fake_folder_id)
    assert response.status_code in (404, 422), response.text

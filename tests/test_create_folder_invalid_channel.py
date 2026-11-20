import uuid
import sender_requests


def test_create_folder_invalid_channel(login):
    fake_id = str(uuid.uuid4())
    folder_body = {"title": "Folder"}
    response = sender_requests.post_create_folder(fake_id, folder_body)
    assert response.status_code in (404, 422), response.text

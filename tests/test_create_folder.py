import uuid
import sender_requests


def test_create_folder_success(channel):
    folder_body = {
        "title": f"Folder {uuid.uuid4()}",
        "description": "Test folder"
    }
    folder_response = sender_requests.post_create_folder(channel, folder_body)
    assert folder_response.status_code == 201, folder_response.text

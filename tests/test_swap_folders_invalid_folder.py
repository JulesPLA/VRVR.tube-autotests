import uuid
import sender_requests


def test_swap_folders_invalid_folder(channel):
    fake_folder_id = str(uuid.uuid4())

    body = {
        "folders": [
            {"folder_id": fake_folder_id, "position": 1}
        ]
    }

    response = sender_requests.post_swap_folders_position(channel, body)
    assert response.status_code in (404, 422)

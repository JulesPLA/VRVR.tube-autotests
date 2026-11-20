import sender_requests


def test_swap_folders_duplicate_positions(channel):
    folder1 = sender_requests.post_create_folder(channel, {"title": "Folder 1"})
    folder2 = sender_requests.post_create_folder(channel, {"title": "Folder 2"})

    assert folder1.status_code == 201, folder1.text
    assert folder2.status_code == 201, folder2.text

    folder1_id = folder1.json()["folder_id"]
    folder2_id = folder2.json()["folder_id"]

    body = {
        "folders": [
            {"folder_id": folder1_id, "position": 1},
            {"folder_id": folder2_id, "position": 1},
        ]
    }

    response = sender_requests.post_swap_folders_position(channel, body)
    assert response.status_code in (400, 409, 422), response.text

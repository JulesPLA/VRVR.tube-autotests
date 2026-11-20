import sender_requests

def test_swap_folders_position(channel):
    folder1 = sender_requests.post_create_folder(channel, {"title": "Folder 1"})
    folder2 = sender_requests.post_create_folder(channel, {"title": "Folder 2"})

    assert folder1.status_code == 201
    assert folder2.status_code == 201

    folder1_id = folder1.json()["folder_id"]
    folder2_id = folder2.json()["folder_id"]

    body = {
        "folders": [
            {"folder_id": folder1_id, "position": 2},
            {"folder_id": folder2_id, "position": 1},
        ]
    }

    swap_response = sender_requests.post_swap_folders_position(channel, body)
    assert swap_response.status_code == 204

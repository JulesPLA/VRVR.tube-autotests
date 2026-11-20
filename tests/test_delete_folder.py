import sender_requests


def test_delete_folder(channel):
    folder_response = sender_requests.post_create_folder(
        channel,
        {"title": "Test Folder"}
    )
    assert folder_response.status_code == 201, folder_response.text
    folder_id = folder_response.json()["folder_id"]

    delete_response = sender_requests.delete_folder(channel, folder_id)
    assert delete_response.status_code == 204

import sender_requests


def test_delete_folder_twice(channel):
    folder_body = {"title": "Test Folder"}
    folder = sender_requests.post_create_folder(channel, folder_body)
    assert folder.status_code == 201, folder.text
    folder_id = folder.json()["folder_id"]

    delete_response = sender_requests.delete_folder(channel, folder_id)
    assert delete_response.status_code == 204

    second_delete = sender_requests.delete_folder(channel, folder_id)
    assert second_delete.status_code in (404, 422), second_delete.text

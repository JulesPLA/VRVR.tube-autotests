import sender_requests


def test_create_folder_without_title(channel):
    folder_body = {"description": "No title"}
    response = sender_requests.post_create_folder(channel, folder_body)
    assert response.status_code == 422, response.text

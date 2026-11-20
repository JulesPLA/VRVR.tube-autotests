import sender_requests


def test_delete_channel_success(channel):
    response = sender_requests.delete_channel(channel)
    assert response.status_code == 204
    assert response.text == ""

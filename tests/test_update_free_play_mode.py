import sender_requests


def test_update_free_play_mode_success(channel):
    update_response = sender_requests.post_free_play_mode(channel, True)
    assert update_response.status_code == 200

    get_response = sender_requests.get_channel(channel)
    assert get_response.json()["is_free_play_mode"] is True

    update_response = sender_requests.post_free_play_mode(channel, False)
    assert update_response.status_code == 200

    get_response = sender_requests.get_channel(channel)
    assert get_response.json()["is_free_play_mode"] is False

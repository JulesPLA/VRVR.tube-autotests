import sender_requests


def test_play_mode_toggle_success(channel):
    r1 = sender_requests.post_play_mode(channel, "singleplay")
    assert r1.status_code == 200

    r2 = sender_requests.post_play_mode(channel, "autoplay")
    assert r2.status_code == 200

import data
import sender_requests


def test_login_success_with_env_credentials():
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    response = sender_requests.post_login(data.login_body)
    assert response.status_code == 200, response.text


def test_login_success_sets_session_cookie():
    response = sender_requests.post_login(data.login_body)
    assert response.status_code == 200, response.text
    auth_cookies = [
        cookie for cookie in sender_requests.session.cookies
        if cookie.name == "Authorization"
    ]
    assert auth_cookies, "Authorization cookie is not set in session"

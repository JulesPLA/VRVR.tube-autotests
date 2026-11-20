import data
import sender_requests


def test_login_invalid_username():
    body = {
        "username": f"wrong_{data.login_body['username']}",
        "password": data.login_body["password"],
    }

    response = sender_requests.post_login(body)
    assert response.status_code in (400, 401, 422), response.text


def test_login_invalid_password():
    body = {
        "username": data.login_body["username"],
        "password": f"{data.login_body['password']}_wrong",
    }

    response = sender_requests.post_login(body)
    assert response.status_code in (400, 401, 422), response.text


def test_login_empty_username():
    body = {"username": "", "password": data.login_body["password"]}
    response = sender_requests.post_login(body)
    assert response.status_code == 422, response.text


def test_login_empty_password():
    body = {"username": data.login_body["username"], "password": ""}
    response = sender_requests.post_login(body)
    assert response.status_code == 422, response.text

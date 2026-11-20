import re
from urllib.parse import urlparse

from playwright.sync_api import expect

import data


def _is_any_error_visible(page, messages, timeout=5000):
    combined = "|".join(re.escape(m) for m in messages)
    error = page.get_by_text(re.compile(combined, re.IGNORECASE)).first
    try:
        expect(error).to_be_visible(timeout=timeout)
        return True
    except AssertionError:
        return False


def test_ui_login_success(login_form, page):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()

    page.wait_for_url(re.compile(r"/channels"), timeout=10000)
    assert urlparse(page.url).path != "/auth/login", f"Still on login page: {page.url}"


def test_ui_login_email_with_spaces_shows_invalid_email(login_form, page):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill(f" {data.login_body['username']} ")
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["Invalid Email address", "Неверный email"],
    ), "Expected invalid email validation message in UI"


def test_ui_login_invalid_email_format_shows_validation_error(login_form, page):
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill("not-an-email")
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["Invalid Email address", "Неверный email"],
    ), "Expected invalid email format validation message in UI"


def test_ui_login_empty_email_shows_required_error(login_form, page):
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill("")
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["The field is required", "Поле обязательно"],
    ), "Expected required-field validation message for empty email"


def test_ui_login_empty_password_shows_required_error(login_form, page):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill("")
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["The field is required", "Поле обязательно"],
    ), "Expected required-field validation message for empty password"


def test_ui_login_wrong_password_shows_auth_error(login_form, page):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill(f"{data.login_body['password']}_wrong")
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["Invalid email or password", "Неверный email или пароль"],
    ), "Expected authentication error for invalid password"


def test_ui_login_wrong_email_and_wrong_password_shows_auth_error(login_form, page):
    login_form["email"].fill("autotest_invalid_user@example.com")
    login_form["password"].fill("invalid_password_123")
    login_form["submit"].click()

    assert _is_any_error_visible(
        page,
        ["Invalid email or password", "Неверный email или пароль"],
    ), "Expected authentication error for invalid email + invalid password"
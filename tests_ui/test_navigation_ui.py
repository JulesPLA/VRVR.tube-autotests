import re

import configuration
import data
from playwright.sync_api import expect


def _login_to_channels(page, login_form):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    page.goto(configuration.UI_LOGIN_URL, wait_until="domcontentloaded")
    page.wait_for_url(re.compile(r"/auth/login"), timeout=20000)

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()
    page.wait_for_url(re.compile(r"/channels"), timeout=20000)


def _first_clickable(candidates, timeout=5000):
    last_exc = None
    for locator in candidates:
        try:
            locator.first.wait_for(state="visible", timeout=timeout)
            return locator.first
        except Exception as exc:
            last_exc = exc
            continue
    raise AssertionError(f"No clickable element found: {last_exc}")


def test_ui_navigation_to_library(page, login_form):
    _login_to_channels(page, login_form)

    link = _first_clickable([
        page.get_by_role("link", name="Library", exact=False),
        page.get_by_text("Library", exact=True),
        page.locator('[data-testid="nav-library"]'),
    ])
    link.click()
    page.wait_for_url(re.compile(r"/contents"), timeout=20000)
    assert "/contents" in page.url.lower(), f"Expected /contents page, got: {page.url}"


def test_ui_navigation_to_devices(page, login_form):
    _login_to_channels(page, login_form)

    link = _first_clickable([
        page.get_by_role("link", name="Devices", exact=False),
        page.get_by_text("Devices", exact=True),
        page.locator('[data-testid="nav-devices"]'),
    ])
    link.click()
    page.wait_for_url(re.compile(r"/devices"), timeout=20000)
    assert "/devices" in page.url.lower(), f"Expected /devices page, got: {page.url}"


def test_ui_navigation_to_account(page, login_form):
    _login_to_channels(page, login_form)

    username_local_part = data.login_body["username"].split("@")[0]

    user_menu = _first_clickable([
        page.get_by_role("button", name=username_local_part, exact=False),
        page.get_by_role("button", name="Account", exact=False),
        page.locator('[data-testid="user-menu"]'),
    ])
    user_menu.click()

    account_link = _first_clickable([
        page.get_by_role("link", name="Account", exact=False),
        page.get_by_text("Account", exact=False),
        page.locator('[data-testid="nav-account"]'),
    ])
    account_link.click()

    page.wait_for_url(re.compile(r"/account"), timeout=20000)
    assert "/account" in page.url.lower(), f"Expected /account page, got: {page.url}"
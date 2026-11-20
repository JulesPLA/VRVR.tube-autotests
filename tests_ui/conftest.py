import re

import pytest

import configuration


def _first_visible(locators, timeout=2000):
    for locator in locators:
        try:
            if locator.count() > 0:
                locator.first.wait_for(state="visible", timeout=timeout)
                return locator.first
        except Exception:
            continue
    return None


@pytest.fixture(scope="session")
def ui_login_url():
    return configuration.UI_LOGIN_URL


@pytest.fixture
def page():
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        pytest.skip(f"Playwright is not installed: {exc}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            yield page
            context.close()
            browser.close()
    except Exception as exc:
        pytest.skip(f"Playwright browser is not available: {exc}")


@pytest.fixture
def login_form(page, ui_login_url):
    page.goto(ui_login_url, wait_until="domcontentloaded")
    page.wait_for_url(re.compile(r"/auth/login"), timeout=15000)
    page.get_by_role("textbox").first.wait_for(timeout=15000)

    email = _first_visible(
        [
            page.get_by_label("Email", exact=False),
            page.get_by_label("E-mail", exact=False),
            page.get_by_label("Логин", exact=False),
            page.locator("input[type='email']"),
            page.locator("input[name='username']"),
            page.get_by_role("textbox").nth(0),
        ]
    )

    password = _first_visible(
        [
            page.get_by_label("Password", exact=False),
            page.get_by_label("Пароль", exact=False),
            page.locator("input[type='password']"),
            page.get_by_role("textbox").nth(1),
        ]
    )

    submit = _first_visible(
        [
            page.get_by_role("button", name="Log in", exact=False),
            page.get_by_role("button", name="Login", exact=False),
            page.get_by_role("button", name="Войти", exact=False),
            page.locator("button[type='submit']"),
        ]
    )

    assert email is not None, "Email field not found on login page"
    assert password is not None, "Password field not found on login page"
    assert submit is not None, "Submit button not found on login page"

    return {"email": email, "password": password, "submit": submit}
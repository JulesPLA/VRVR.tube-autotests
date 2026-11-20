import re
from urllib.parse import urlparse

import data


def test_ui_login_redirects_to_channels(login_form, page):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()

    page.wait_for_url(re.compile(r"/channels"), timeout=20000)
    assert urlparse(page.url).path.startswith("/channels"), (
        f"Expected redirect to channels page, got: {page.url}"
    )
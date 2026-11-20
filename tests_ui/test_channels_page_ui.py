import re
import uuid

import pytest
from playwright.sync_api import expect

import data
import sender_requests


def _login_to_channels(page, login_form):
    assert data.login_body["username"], "Set VRVR_USERNAME in .env"
    assert data.login_body["password"], "Set VRVR_PASSWORD in .env"

    login_form["email"].fill(data.login_body["username"])
    login_form["password"].fill(data.login_body["password"])
    login_form["submit"].click()
    page.wait_for_url(re.compile(r"/channels"), timeout=20000)

    page.get_by_role(
        "searchbox", name="Search by channel name", exact=False
    ).wait_for(timeout=20000)


@pytest.fixture
def created_channels():
    sender_requests.post_login(data.login_body)

    title_a = f"UI_A_{uuid.uuid4()}"
    title_b = f"UI_B_{uuid.uuid4()}"

    response_a = sender_requests.post_create_channel({"title": title_a})
    response_b = sender_requests.post_create_channel({"title": title_b})

    assert response_a.status_code == 201, response_a.text
    assert response_b.status_code == 201, response_b.text

    channel_a = {"id": response_a.json()["channel_id"], "title": title_a}
    channel_b = {"id": response_b.json()["channel_id"], "title": title_b}

    yield channel_a, channel_b

    sender_requests.delete_channel(channel_a["id"])
    sender_requests.delete_channel(channel_b["id"])


def test_ui_channels_search_full_partial_and_empty_result(page, login_form, created_channels):
    channel_a, channel_b = created_channels
    _login_to_channels(page, login_form)

    search = page.get_by_role("searchbox", name="Search by channel name", exact=False)
    link_a = page.get_by_role("link", name=channel_a["title"], exact=True)
    link_b = page.get_by_role("link", name=channel_b["title"], exact=True)

    # Full title search should return the target channel only.
    search.fill(channel_a["title"])
    expect(link_a).to_be_visible(timeout=5000)

    # Switching the full query to another channel should show that channel.
    search.fill(channel_b["title"])
    expect(link_b).to_be_visible(timeout=5000)

    # Partial title search should also find the same channel.
    partial = channel_a["title"][-8:]
    search.fill(partial)
    expect(link_a).to_be_visible(timeout=5000)

    # Non-existing query should return empty result for our channels.
    search.fill("NO_SUCH_CHANNEL_123456789")
    expect(link_a).to_be_hidden(timeout=5000)
    expect(link_b).to_be_hidden(timeout=5000)


def test_ui_channels_search_reset_restores_results(page, login_form, created_channels):
    channel_a, channel_b = created_channels
    _login_to_channels(page, login_form)

    search = page.get_by_role("searchbox", name="Search by channel name", exact=False)
    link_a = page.get_by_role("link", name=channel_a["title"], exact=True)
    link_b = page.get_by_role("link", name=channel_b["title"], exact=True)

    # Дождаться, что список каналов реально отрисовался до начала поиска.
    expect(link_a).to_be_visible(timeout=10000)

    search.fill("NO_SUCH_CHANNEL_123456789")
    expect(link_a).to_be_hidden(timeout=10000)
    expect(link_b).to_be_hidden(timeout=10000)

    # Clear search and ensure list is restored (known channels appear again).
    search.fill("")
    expect(link_a).to_be_visible(timeout=10000)
    expect(link_b).to_be_visible(timeout=10000)


def test_ui_open_channel_from_list(page, login_form, created_channels):
    channel_a, _ = created_channels
    _login_to_channels(page, login_form)

    search = page.get_by_role("searchbox", name="Search by channel name", exact=False)
    search.fill(channel_a["title"])

    link_a = page.get_by_role("link", name=channel_a["title"], exact=True)
    expect(link_a).to_be_visible(timeout=5000)
    link_a.first.click()

    page.wait_for_url(re.compile(r"/channels/"), timeout=10000)
    assert "/channels/" in page.url.lower(), f"Expected channel details URL, got: {page.url}"
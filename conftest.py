import pytest
from playwright.sync_api import sync_playwright
from utils.credentials import get_credentials
import time

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture
def context(browser):
    username, password = get_credentials("FB_TEST")
    context = browser.new_context(
        http_credentials={
            "username": username,
            "password": password
        }
    )
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    page.set_default_timeout(10_000)
    yield page
    # Debug
    time.sleep(10)
    page.close()

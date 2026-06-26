"""
Pytest fixtures for UI testing.
"""
import pytest  # type: ignore[reportMissingImports]
import logging
from config import cfg, pages
from utilities.web_client import WebClient
from utilities.auth import WebAuthManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session")
def browser():
    client = WebClient()
    yield client
    client.close()

@pytest.fixture
def auth(browser):
    return WebAuthManager(browser)

@pytest.fixture
def manager(auth):
    auth.login("manager")
    return auth

@pytest.fixture
def teller(auth):
    auth.login("teller")
    return auth

@pytest.fixture
def open_branch(browser, manager):
    """Ensures branch is OPEN before test runs."""
    from utilities.helpers import build_open_form
    browser.submit_form(pages.BRANCH_OPEN, build_open_form())
    yield browser
    # Cleanup: Attempt to close branch
    from utilities.helpers import build_close_form
    browser.submit_form(pages.BRANCH_CLOSE, build_close_form())

@pytest.fixture
def closed_branch(browser, manager):
    """Ensures branch is CLOSED before test runs."""
    from utilities.helpers import build_close_form
    browser.submit_form(pages.BRANCH_CLOSE, build_close_form())
    yield browser
    
@pytest.fixture
def capture(browser, request):
    yield

    name = request.node.name
    browser.save_screenshot(f"reports/screenshots/{name}.png")

results = []

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        results.append({
            "name": item.name,
            "status": rep.outcome,
            "duration": rep.duration,
        })
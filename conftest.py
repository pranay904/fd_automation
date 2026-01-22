import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.fixture(scope="session")
def user_email():
    """
    Stores registered email to reuse in login test
    """
    return {}

@pytest.fixture(params=["chromium", "firefox", "edge"])
def page(request):
    with sync_playwright() as p:
        if request.param == "chromium":
            browser = p.chromium.launch(headless=False)
        elif request.param == "firefox":
            browser = p.firefox.launch(headless=False)
        else:
            browser = p.chromium.launch(channel="msedge", headless=False)

        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs("reports/screenshots", exist_ok=True)
            page.screenshot(path=f"reports/screenshots/{item.name}.png")

import pytest
import os
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page(request):
    browser_name = getattr(request, "param", "chromium")
    with sync_playwright() as p:
        if browser_name == "firefox":
            browser = p.firefox.launch(headless=False, slow_mo=100)
        elif browser_name == "edge":
            browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=100)
        else:
            browser = p.chromium.launch(headless=False, slow_mo=100)

        context = browser.new_context(viewport={"width": 1280, "height": 800})
        pg = context.new_page()

        yield pg

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call=None):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        pg = item.funcargs.get("page")
        if pg:
            screenshots_dir = os.path.join("FD", "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
            try:
                pg.screenshot(path=screenshot_path)
                print(f"[Screenshot saved] {screenshot_path}")
            except Exception as e:
                print(f"[Screenshot failed] {e}")

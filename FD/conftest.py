import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture(scope="session")
def user_email():
    """
    Stores registered email to reuse in login test
    """
    return {}


@pytest.fixture(params=["chromium", "firefox", "edge"],scope="session")
def page(request):
    with sync_playwright() as p:
        if request.param == "chromium":
            browser = p.chromium.launch(headless=False)

        elif request.param == "firefox":
            browser = p.firefox.launch(headless=False)

        else:  # edge
            browser = p.chromium.launch(channel="msedge", headless=False)

        context = browser.new_context()
        page = context.new_page()

        yield page

        context.close()
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

#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("page")
#         if page:
#             os.makedirs("reports/screenshots", exist_ok=True)
#             page.screenshot(path=f"reports/screenshots/{item.name}.png")


# conftest.py
# import pytest
# import os
# from playwright.sync_api import sync_playwright
#
# @pytest.fixture(scope="session")
# def browser_context():
#     """Launch browser context once per session"""
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # You can set `headless=True` for headless mode
#         context = browser.new_context()
#         yield context
#         browser.close()
#
# @pytest.fixture(scope="function")
# def page(browser_context):
#     """Provide a fresh page per test function"""
#     page = browser_context.new_page()
#
#     # Set up listeners for console & network
#     page.on("console", lambda msg: print(f"[Console {msg.type}] {msg.text}"))
#     page.on("request", lambda req: print(f"[Request] {req.method} {req.url}"))
#     page.on("response", lambda res: print(f"[Response {res.status}] {res.url}"))
#
#     yield page
#     page.close()  # Close page but keep browser alive
#
# # Hook to take screenshot on failure
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("page")
#         if page:
#             os.makedirs("reports/screenshots", exist_ok=True)
#             screenshot_path = f"reports/screenshots/{item.name}.png"
#             try:
#                 page.screenshot(path=screenshot_path)
#                 print(f"[Screenshot saved] {screenshot_path}")
#             except Exception as e:
#                 print(f"[Screenshot failed] {e}")


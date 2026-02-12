import os
import datetime
import pytest
from pytest_html import extras
from playwright.sync_api import sync_playwright
from utils.highlight_helpers import enable_click_highlight

# Base folder
BASE_DIR = "reports"

# Subfolders for videos, screenshots, API and console logs
DIRS = {
    "videos": os.path.join(BASE_DIR, "videos"),
    "screenshots": os.path.join(BASE_DIR, "screenshots"),
    "api": os.path.join(BASE_DIR, "api_logs"),
    "console": os.path.join(BASE_DIR, "console_logs")
}

# Make sure folders exist
for path in DIRS.values():
    os.makedirs(path, exist_ok=True)

# ---------------------------
# Pytest fixture for Playwright page
# ---------------------------
@pytest.fixture
def page(request):
    api_logs = []
    console_logs = []

    with sync_playwright() as p:
        # Launch browser maximized
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1500,
            args=["--start-maximized"]
        )

        # Full screen browser context with video
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=DIRS["videos"],
            record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        enable_click_highlight(page)

        # Capture console & API logs
        page.on("console", lambda m: console_logs.append(f"{m.type.upper()} - {m.text}"))
        page.on("request", lambda r: api_logs.append(f"REQ {r.method} {r.url}"))
        page.on("response", lambda r: api_logs.append(f"RES {r.status} {r.url}"))

        # Print logs live in terminal
        page.on("console", lambda m: print(f"CONSOLE: {m.type.upper()} - {m.text}"))
        page.on("request", lambda r: print(f"REQ: {r.method} {r.url}"))
        page.on("response", lambda r: print(f"RES: {r.status} {r.url}"))

        # Attach logs to pytest node
        request.node.api_logs = api_logs
        request.node.console_logs = console_logs

        yield page

        # Screenshot on failure
        test_name = request.node.name
        if request.node.rep_call.failed:
            screenshot_path = os.path.join(DIRS["screenshots"], f"{test_name}_FAILED.png")
            page.screenshot(path=screenshot_path)
            request.node.screenshot_path = screenshot_path

        # Save API logs to file
        api_file = os.path.join(DIRS["api"], f"{test_name}_api.log")
        with open(api_file, "w", encoding="utf-8") as f:
            f.write("\n".join(api_logs))

        # Save console logs to file
        console_file = os.path.join(DIRS["console"], f"{test_name}_console.log")
        with open(console_file, "w", encoding="utf-8") as f:
            f.write("\n".join(console_logs))

        context.close()
        browser.close()

# ---------------------------
# Hook to attach logs/screenshots to HTML
# ---------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        extras_list = []

        if hasattr(item, "api_logs"):
            extras_list.append(extras.text("\n".join(item.api_logs), name="API Logs"))

        if hasattr(item, "console_logs"):
            extras_list.append(extras.text("\n".join(item.console_logs), name="Console Logs"))

        if rep.failed and hasattr(item, "screenshot_path"):
            extras_list.append(extras.image(item.screenshot_path, name="Failure Screenshot"))

        # Attach the extras to the report
        rep.extras = extras_list

# ---------------------------
# Automatically generate timestamped HTML report
# ---------------------------
def pytest_configure(config):
    if not config.option.htmlpath:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        config.option.htmlpath = os.path.join(BASE_DIR, f"report_{timestamp}.html")

import pytest
import os
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome, firefox, edge"
    )


def launch_browser(playwright, browser_name):

    if browser_name == "firefox":

        return playwright.firefox.launch(
            headless=False
        )

    elif browser_name == "edge":

        return playwright.chromium.launch(
            channel="msedge",
            headless=False,
            args=["--start-maximized"]
        )

    else:
        # Default Chrome
        return playwright.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--start-maximized"]
        )


def add_block_overlay(context):

    context.add_init_script("""
        const _block = () => {
            const style = document.createElement('style');
            style.id = '__block_netcore__';
            style.textContent = `
                #smt-overlay, #st_notification_banner, div[smtmsgid],
                [id^='smt'], [class*='smt-block'], [class*='smt-close'] {
                    display: none !important;
                    pointer-events: none !important;
                    visibility: hidden !important;
                    z-index: -9999 !important;
                }
            `;

            if (!document.getElementById('__block_netcore__')) {
                (document.head || document.documentElement)
                .appendChild(style);
            }
        };

        _block();

        new MutationObserver(_block)
        .observe(document.documentElement, {
            childList: true,
            subtree: true
        });
    """)


@pytest.fixture(scope="function")
def page(request):

    playwright = sync_playwright().start()

    browser_name = request.config.getoption("--browser")

    browser = launch_browser(
        playwright,
        browser_name
    )

    context = browser.new_context(
        no_viewport=True
    )

    add_block_overlay(context)

    pg = context.new_page()

    yield pg

    try:
        context.close()
    except Exception:
        pass

    try:
        browser.close()
    except Exception:
        pass

    try:
        playwright.stop()
    except Exception:
        pass



# Session scoped browser
@pytest.fixture(scope="session")
def shared_page(request):

    playwright = sync_playwright().start()

    browser_name = request.config.getoption("--browser")

    browser = launch_browser(
        playwright,
        browser_name
    )

    context = browser.new_context(
        no_viewport=True
    )

    add_block_overlay(context)

    pg = context.new_page()

    yield pg

    try:
        context.close()
    except Exception:
        pass

    try:
        browser.close()
    except Exception:
        pass

    try:
        playwright.stop()
    except Exception:
        pass



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call=None):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        pg = item.funcargs.get("page") or item.funcargs.get("shared_page")

        if pg:

            base_dir = os.path.dirname(os.path.abspath(__file__))

            screenshots_dir = os.path.join(
                base_dir,
                "reports",
                "screenshots"
            )

            os.makedirs(
                screenshots_dir,
                exist_ok=True
            )

            screenshot_path = os.path.join(
                screenshots_dir,
                f"{item.name}.png"
            )

            try:
                pg.screenshot(path=screenshot_path)
                print(f"[Screenshot saved] {screenshot_path}")

            except Exception as e:
                print(f"[Screenshot failed] {e}")


def pytest_sessionfinish(session, exitstatus):

    """Safety net — export report even if session is interrupted."""

    try:
        from FD.tests.Regression.test_quiz_flow import report
        report.export()

    except Exception:
        pass
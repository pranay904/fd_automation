import pytest
import os
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page(request):
    # Chromium only, headless=True for speed
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    # Block Netcore overlay before any page loads
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
                (document.head || document.documentElement).appendChild(style);
            }
        };
        _block();
        new MutationObserver(_block).observe(document.documentElement, {childList: true, subtree: true});
    """)
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
        pg = item.funcargs.get("page")
        if pg:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            screenshots_dir = os.path.join(base_dir, "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}.png")
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

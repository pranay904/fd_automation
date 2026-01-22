from playwright.sync_api import Playwright, expect


def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://friendlydiamonds.com/")

    page.get_by_text(
        "Get FREE lab diamond jewelry on purchases over $1,000. Claim yours at checkout."
    ).click()

    page.get_by_role("link", name="About").click()

    page.get_by_role("heading", name="The ‘Friendly’ Service").click()
    page.get_by_role("heading", name="The ‘Friendly’ Diamond").click()

    page.get_by_text("We’re not just showcasing").click()

    expect(page.locator("#planet video")).to_be_visible()

    context.close()
    browser.close()

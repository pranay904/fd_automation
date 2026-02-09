from playwright.sync_api import Page, Locator

class UIHelpers:
    def __init__(self, page: Page):
        self.page = page

    def fill_text(self, locator: Locator, text: str):
        locator.fill("")     # clear
        locator.fill(text)   # paste text

    def click_search(self, locator: Locator):
        locator.click()
        self.page.wait_for_load_state("networkidle")

    def select_dropdown(self, locator: Locator, value: str):
        locator.select_option(value)

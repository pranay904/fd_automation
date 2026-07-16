import time
from playwright.sync_api import expect

def retry_until_true(param, timeout, error_msg):
    pass


class BasePage:
    def __init__(self, page):
        self.page = page

    def open_url(self, url):


        self.page.goto(url)

    def click(self, locator):
        self.page.click(locator)

    def fill(self, locator, value):
        self.page.fill(locator, value)

    def fills(self, locator, value):
        self.page.locator(locator).fill(str(value))

    def get_texts(self, locator):
        return [t.strip() for t in self.page.locator(locator).all_inner_texts()]

    def navigation_Back(self):
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")

    def navigate_forward(self):
        self.page.go_forward()
        self.page.wait_for_load_state("networkidle")

    def reload(self):
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def wait_for_network_idle(self):
        self.page.wait_for_load_state("networkidle")

    def wait_for_element_visible(self, locator, timeout=10):
        retry_until_true(
            lambda: self.page.locator(locator).is_visible(),
            timeout=timeout,
            error_msg=f"Element not visible: {locator}"
        )

    def text(self, locator):
        return self.page.locator(locator).inner_text()

    def visible(self, locator):
        expect(self.page.locator(locator)).to_be_visible()

    def wait(self):
        self.page.wait_for_load_state("networkidle")





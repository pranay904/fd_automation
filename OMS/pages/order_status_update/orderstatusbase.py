import time
from playwright.sync_api import expect


class OrderStatusBase:

    def __init__(self, page):
        self.page = page
        self.global_delay = 1500   # 1.5 sec delay


    # Utility Methods (Reusable)


    def wait_delay(self):
        self.page.wait_for_timeout(self.global_delay)

    def highlight(self, locator):
        locator.evaluate("""
            element => {
                element.style.border = '3px solid red';
                element.style.transition = '0.3s';
            }
        """)

    def click_with_effect(self, locator):
        locator.wait_for(state="visible")
        self.highlight(locator)
        locator.click()
        self.wait_delay()

    def fill_with_effect(self, locator, value):
        locator.wait_for(state="visible")
        self.highlight(locator)
        locator.fill(value)
        self.wait_delay()

    def hover_with_effect(self, locator):
        locator.wait_for(state="visible")
        self.highlight(locator)
        locator.click()
        self.wait_delay()



    # Open Order Lines page


    def open_order_and_all_order_line(self):

        self.page.locator(".v-navigation-drawer__content").hover()

        order_lines = self.page.locator(
            "//div[@class='v-list-item-title'][normalize-space()='Order Lines']"
        )
        self.click_with_effect(order_lines)

        all_order_lines = self.page.locator(
            "(//div[contains(text(),'All Order Lines')])[1]"
        )
        self.click_with_effect(all_order_lines)

        panel = self.page.locator(
            "(//span[@class='v-expansion-panel-title__overlay'])[1]"
        )
        self.click_with_effect(panel)


    # Click Order Status Update Button


    def click_on_order_status_update(self):

        button = self.page.get_by_role("button", name="Order-status-Update")
        self.click_with_effect(button)

        expect(self.page.get_by_text("Update Order")).to_have_text("Update Order")

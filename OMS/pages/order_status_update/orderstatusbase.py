import time
from playwright.sync_api import expect

class OrderStatusBase:
    def __init__(self, page):
        self.page = page

    # -------------------------------
    # Open Order Lines page
    # -------------------------------
    def open_order_and_all_order_line(self):
        self.page.locator(".v-navigation-drawer__content").hover()
        self.page.locator("//div[@class='v-list-item-title'][normalize-space()='Order Lines']").click()
        self.page.locator("(//div[contains(text(),'All Order Lines')])[1]").click()
        self.page.locator("(//span[@class='v-expansion-panel-title__overlay'])[1]").click()

    # -------------------------------
    # Click on Order Status Update button
    # -------------------------------
    def click_on_order_status_update(self):
        self.page.get_by_role("button", name="Order-status-Update").click()
        # Verify the text
        expect(self.page.get_by_text("Update Order")).to_have_text("Update Order")

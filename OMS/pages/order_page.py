import re
from utils.ui_helpers import UIHelpers
import time

class OrderPage:
    def __init__(self, page):
        self.page = page
        self.ui = UIHelpers(page)

        # Inputs
        self.order_id_input = page.get_by_role("textbox", name="Order-Id")
        self.order_ref_input = page.get_by_role("textbox", name=re.compile("order-ref", re.I))
        self.customer_name_input = page.get_by_role("textbox", name="Customer Name")
        self.customer_email_input = page.get_by_role("textbox", name="Customer Email")

        # Dropdowns
        self.order_status_dropdown = page.locator("(//div[@class='v-field__input'])[1]")
        self.priority_dropdown = page.locator("(//div[@class='v-field__input'])[2]")

        # Search button
        self.search_button = page.get_by_role("button", name=re.compile("search", re.I))
        self.order_id_input = page.get_by_role("textbox", name="Order-Id")
        self.search_button = page.get_by_role("button", name=re.compile("search", re.I))
        self.click_on_search = page.locator(".v-expansion-panel-title__overlay")

    def open_order(self):
        self.page.locator(".v-navigation-drawer__content").hover()
        self.page.locator("(//div[contains(text(),'Orders')])[1]").click()
        time.sleep(3)

    def get_first_n_order_ids(self, count=5):
        """Get first N Order IDs from table rows"""
        order_ids = []

        rows = self.page.locator("button.v-expansion-panel-title")

        for i in range(min(count, rows.count())):
            row = rows.nth(i)
            order_id = row.locator("div.table_data").nth(0).inner_text()
            order_ids.append(order_id)

        return order_ids

    def search_order(self, order_id):
        self.order_id_input.fill(order_id)
        self.search_button.click()
        self.click_on_search.click()
        self.page.wait_for_load_state("networkidle")

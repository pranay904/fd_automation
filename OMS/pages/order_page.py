import re
from utils.ui_helpers import UIHelpers
import time

class OrderPage:
    def __init__(self, page):
        self.page = page
        self.ui = UIHelpers(page)

        # Inputs
        self.order_id_input = page.get_by_role("textbox", name="Order-Id")
        self.order_ref_input = page.get_by_role("textbox", name="Order-Ref")
        self.customer_name_input = page.get_by_role("textbox", name="Customer Name")
        self.customer_email_input = page.get_by_role("textbox", name="Customer Email")

        # Removed filter button
        self.removed_filter = page.locator(
            "//i[@class='mdi-close mdi v-icon notranslate v-theme--light v-icon--size-default v-icon--clickable close-icon ms-3']"
        )

        # Dropdowns
        self.order_status_dropdown = page.locator("(//div[@class='v-field__input'])[1]")
        self.priority_dropdown = page.locator("(//div[@class='v-field__input'])[2]")

        # Buttons
        self.search_button = page.get_by_role("button", name=re.compile("search", re.I))
        self.reset_button = page.get_by_role("button", name="Reset Filter")
        self.click_on_search = page.locator(".v-expansion-panel-title__overlay")

    # -------------------------------
    # Open Orders Page
    # -------------------------------
    def open_order(self):
        self.page.locator(".v-navigation-drawer__content").hover()
        self.page.locator("(//div[contains(text(),'Orders')])[1]").click()
        time.sleep(3)

    # -------------------------------
    # Get first N Order IDs
    # -------------------------------
    def get_first_n_order_ids(self, count=5):
        order_ids = []
        rows = self.page.locator("button.v-expansion-panel-title")
        for i in range(min(count, rows.count())):
            row = rows.nth(i)
            order_id = row.locator("div.table_data").nth(0).inner_text()
            order_ids.append(order_id)
        return order_ids

    # -------------------------------
    # Search by Order ID
    # -------------------------------
    def search_order_by_id(self, order_id):
        self.order_id_input.fill(order_id)
        self.search_button.click()
        self.click_on_search.click()
        self.page.wait_for_load_state("networkidle")
        # Remove filter after search
        self.removed_filter.click()
        self.page.wait_for_load_state("networkidle")

    # -------------------------------
    # Get first N Order Refs (just copy/store)
    # -------------------------------
    def get_first_n_order_refs(self, count=5):
        """
        Click copy icon and return list of order ref texts.
        """
        order_refs = []
        rows = self.page.locator("button.v-expansion-panel-title")

        for i in range(min(count, rows.count())):
            row = rows.nth(i)
            order_ref_cell = row.locator("div.table_data").nth(1)
            copy_icon = order_ref_cell.locator("i[role='button']")

            # Click copy icon (video clarity)
            copy_icon.wait_for(state="visible", timeout=5000)
            copy_icon.click()

            # Get text from cell
            order_ref_text = order_ref_cell.inner_text().split()[0]
            order_refs.append(order_ref_text)

        return order_refs

    # -------------------------------
    # Search by Order Ref (fill input, search, reset)
    # -------------------------------
    def search_order_by_ref(self, order_ref_text, delay=1.5):
        """
        Fill Order-Ref input with given text, search, reset, and wait.
        """
        self.order_ref_input.fill(order_ref_text)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

        # Reset filter
        self.reset_button.click()
        self.page.wait_for_load_state("networkidle")

        # Optional delay
        time.sleep(delay)

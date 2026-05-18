import time

from OMS.pages.POS.base_pos import BasePOS

class CreateCYOOrderPOS:
    def __init__(self, page):
        self.page = page
        self.base_pos = BasePOS(page)

        self.Setting_sku = "AFDRE11200"
        self.Diamonds_ID = "D47004"

    def select_store_list(self):
        stores = self.base_pos.store_list()
        stores["Ny_store"].click()
        # Wait until store selection updates UI
        self.page.wait_for_timeout(500)

    def select_product_type(self):
        product_type = self.base_pos.product_type()
        product_type["Cyo"].click()
        product_type["Cyo_Ring"].click()

    def search_setting_sku(self):
        settings_sku = self.page.locator("(//div[@class='v-field__input']//input)[2]")
        settings_sku.fill(self.Setting_sku)

        # Wait dynamically until suggestions appear
        suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[contains(@class,'v-list-item')]"
        )
        try:
            suggestions.first.wait_for(state="visible", timeout=None)  # Wait indefinitely until visible
            suggestions.first.click(force=True)
        except:
            print("No suggestions appeared - skipping selection")
            return

        # Wait for "Add Appraisal" checkbox dynamically
        checkbox = self.page.get_by_text("Add Appraisal", exact=True)
        checkbox.wait_for(state="visible", timeout=None)
        checkbox.click(force=True)

    def select_ring_size(self):
        size_input = self.page.locator("(//div[@class='v-field__input']//input)[3]")
        size_input.click(force=True)

        # Wait dynamically for ring size suggestions
        size_suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[contains(@class,'v-list-item')]"
        )
        try:
            size_suggestions.first.wait_for(state="visible", timeout=None)
            size_suggestions.first.click(force=True)
            # Always select the first suggestion
        except:
            print("No ring size suggestions found - skipping selection")
            return
        time.sleep(2)

        # Print selected ring size
        selected_value = size_input.input_value()
        print(f"Selected ring size: {selected_value}")

    def search_diamond_sku(self):
        diamonds_sku = self.page.locator("(//div[@class='v-field__input']//input)[4]")
        diamonds_sku.click()
        diamonds_sku.fill(self.Diamonds_ID)

        # Wait for suggestions to appear
        suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[@role='option']"
        )

        # Wait until at least 2 options are visible
        suggestions.nth(1).wait_for(state="visible")

        # Select second option
        suggestions.nth(1).click()
        time.sleep(1)

        # Click ADD button dynamically
        add_button = self.page.get_by_role("button", name="ADD")
        add_button.wait_for(state="visible", timeout=None)
        add_button.click()
        time.sleep(2)

        view_products = self.page.locator("(//div[@class='v-col-md-6 v-col-12'])[4]")
        view_products.scroll_into_view_if_needed()
        view_products.click()

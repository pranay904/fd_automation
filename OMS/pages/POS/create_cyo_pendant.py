from OMS.pages.POS.base_pos import BasePOS


class CreateCYOPendantOrderPOS:
    def __init__(self, page):
        self.page = page
        self.base_pos = BasePOS(page)

        self.Setting_sku = "AFDP204"
        self.Diamonds_ID = "D47004"

    def select_store_list(self):
        stores = self.base_pos.store_list()
        stores["Ny_store"].click()
        self.page.wait_for_timeout(500)

    def select_product_type(self):
        product_type = self.base_pos.product_type()
        product_type["Cyo"].click()
        product_type["Cyo_Pendant"].click()

    def search_setting_sku(self):
        settings_sku = self.page.locator("(//div[@class='v-field__input']//input)[2]")
        settings_sku.fill(self.Setting_sku)

        suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[contains(@class,'v-list-item')]"
        )

        suggestions.first.wait_for(state="visible")
        suggestions.first.click(force=True)

        checkbox = self.page.get_by_text("Add Appraisal", exact=True)
        checkbox.wait_for(state="visible")
        checkbox.click(force=True)

    # NEW METHOD
    def select_chain_length(self):
        chain_input = self.page.locator("(//div[@class='v-field__input']//input)[3]")
        chain_input.click(force=True)

        chain_options = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[@role='option']"
        )

        chain_options.first.wait_for(state="visible")
        chain_options.first.click(force=True)

        selected_value = chain_input.input_value()
        print(f"Selected chain length: {selected_value}")

    def search_diamond_sku(self):
        diamonds_sku = self.page.locator("(//div[@class='v-field__input']//input)[4]")
        diamonds_sku.click()
        diamonds_sku.fill(self.Diamonds_ID)

        suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[@role='option']"
        )

        suggestions.nth(1).wait_for(state="visible")
        suggestions.nth(1).click()

        add_button = self.page.get_by_role("button", name="ADD")
        add_button.wait_for(state="visible")
        add_button.click()

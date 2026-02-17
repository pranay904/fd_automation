from OMS.pages.POS.base_pos import BasePOS


class CreateDiamondOrderPOS:
    def __init__(self, page):
        self.page = page
        self.base_pos = BasePOS(page)

        self.Diamonds_ID = "D47004"

    def select_store_list(self):
        stores = self.base_pos.store_list()
        stores["Ny_store"].click()
        self.page.wait_for_timeout(500)

    def select_product_type(self):
        product_type = self.base_pos.product_type()
        product_type["Diamond"].click()


    def search_diamond_sku(self):
        diamonds_sku = self.page.locator("(//div[@class='v-field__input']//input)[2]")
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


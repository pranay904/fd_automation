from OMS.pages.POS.base_pos import BasePOS


class CreateJewelryOrderPOS:

    def __init__(self, page):
        self.page = page
        self.base_pos = BasePOS(page)
        self.slug = None
        self.SKU = "R14004"

    # global wait
        self.global_delay = 1500

    # Utility Methods

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
        locator.wait_for(state="visible", timeout=10000)
        self.highlight(locator)
        locator.click()
        self.wait_delay()

    def fill_with_effect(self, locator, value):
        locator.wait_for(state="visible", timeout=10000)
        self.highlight(locator)
        locator.fill(value)
        self.wait_delay()

    # Store & Product Selection

    def select_store_list(self):
        stores = self.base_pos.store_list()
        self.click_with_effect(stores["Ny_store"])

    def select_product_type(self):
        product_type = self.base_pos.product_type()
        self.click_with_effect(product_type["Jewelry"])


    def search_jewelry_sku(self):

        settings_sku = self.page.locator("(//div[@class='v-field__input']//input)[2]")
        self.fill_with_effect(settings_sku, self.SKU)

        suggestions = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[contains(@class,'v-list-item')]"
        )

        try:
            suggestions.first.wait_for(state="visible", timeout=10000)
            self.click_with_effect(suggestions.first)
        except:
            print("No suggestions appeared - skipping selection")
            return

        checkbox = self.page.get_by_text("Add Appraisal", exact=True)
        self.click_with_effect(checkbox)

    def select_ring_size(self):

        size_dropdown = self.page.locator("//div[@aria-haspopup='listbox']")
        self.click_with_effect(size_dropdown)

        size_options = self.page.locator(
            "//div[contains(@class,'v-overlay-container')]//div[contains(@class,'v-list-item')]"
        )

        try:
            size_options.first.wait_for(state="visible", timeout=10000)
            self.click_with_effect(size_options.first)
        except:
            print("No ring size suggestions found - skipping selection")
            return

        size_input = self.page.locator("//div[@aria-haspopup='listbox']//input")
        selected_value = size_input.input_value()
        print(f"Selected Jewelry ring size: {selected_value}")

        add_button = self.page.get_by_role("button", name="ADD")
        self.click_with_effect(add_button)

        view_products = self.page.locator("//body/div/div/main/div/div/div/div/div/div[2]")
        view_products.scroll_into_view_if_needed()
        actual_product = self.page.locator("//div[@class='w-100']")
        actual_product.scroll_into_view_if_needed()
        self.wait_delay()

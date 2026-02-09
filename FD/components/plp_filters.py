from components.base_filters import BaseFilters


class PLPFilters(BaseFilters):

    # ---------------- PLP LOCATORS ----------------
    PLP_PRODUCTS = "//div[@class='product_box']"
    PLP_MOB_MOD = ".//*[contains(@class,'mob_mod')]//a[1]"
    PLP_PRICE = ".//h4[contains(@class,'mb-3')]"
    PLP_PRODUCT_LINK = ".//a[1]"
    PLP_ACTIVE_METAL = ".//div[contains(@class,'metal_color')]//div[contains(@class,'metal_box') and contains(@class,'active')]"

    def get_products(self, count=5):
        products = self.page.locator(self.PLP_PRODUCTS)
        return products, min(count, products.count())

    def validate_active_metal(self, product, expected_metal):
        expected_color = expected_metal.split()[-2].lower()
        active_class = product.locator(
            "xpath=" + self.PLP_ACTIVE_METAL
        ).get_attribute("class")

        assert expected_color in active_class, (
            f"Metal mismatch: expected {expected_color}, got {active_class}"
        )

    # def open_product(self, product):
    #     self.page.evaluate(
    #         "el => el.scrollIntoView({block:'center'})", product
    #     )
    #     self.page.wait_for_timeout(1000)
    #     product.locator("xpath=" + self.PLP_PRODUCT_LINK).click()
    #     self.page.wait_for_timeout(3000)

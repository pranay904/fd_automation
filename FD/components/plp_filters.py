
class PLPPage:

    def __init__(self, page):
        self.page = page

        # First product
        self.product_box = "(//div[contains(@class,'product')])[1]"

        self.product_metal = "(//div[contains(@class,'product')])[1]//span[contains(@class,'metal')]"
        self.product_shape = "(//div[contains(@class,'product')])[1]//span[contains(@class,'shape')]"
        self.product_style = "(//div[contains(@class,'product')])[1]//span[contains(@class,'style')]"
        self.product_carat = "(//div[contains(@class,'product')])[1]//span[contains(@class,'carat')]"
        self.product_price = "(//div[contains(@class,'product')])[1]//span[contains(@class,'price')]"
        self.product_mrp = "(//div[contains(@class,'product')])[1]//span[contains(@class,'mrp')]"

    def get_first_product_details(self):

        return {
            "metal": self.page.locator(self.product_metal).inner_text(),
            "shape": self.page.locator(self.product_shape).inner_text(),
            "style": self.page.locator(self.product_style).inner_text(),
            "carat": self.page.locator(self.product_carat).inner_text(),
            "price": self.page.locator(self.product_price).inner_text(),
            "mrp": self.page.locator(self.product_mrp).inner_text(),
        }

    def open_first_product(self):
        self.page.locator(self.product_box).click()

    def normalize_price(self, text):

        if not text:
            return 0

        text = text.replace("$", "").replace("£", "")
        text = text.replace(",", "").strip()

        return int(float(text))





# from FD.components.base_filters import BaseFilters
#
#
# class PLPFilters(BaseFilters):
#
#     # ---------------- PLP LOCATORS ----------------
#     PLP_PRODUCTS = "//div[@class='product_box']"
#     PLP_MOB_MOD = ".//*[contains(@class,'mob_mod')]//a[1]"
#     PLP_PRICE = ".//h4[contains(@class,'mb-3')]"
#     PLP_PRODUCT_LINK = ".//a[1]"
#     PLP_ACTIVE_METAL = ".//div[contains(@class,'metal_color')]//div[contains(@class,'metal_box') and contains(@class,'active')]"
#
#     def get_products(self, count=5):
#         products = self.page.locator(self.PLP_PRODUCTS)
#         return products, min(count, products.count())
#
#     def validate_active_metal(self, product, expected_metal):
#         expected_color = expected_metal.split()[-2].lower()
#         active_class = product.locator(
#             "xpath=" + self.PLP_ACTIVE_METAL
#         ).get_attribute("class")
#
#         assert expected_color in active_class, (
#             f"Metal mismatch: expected {expected_color}, got {active_class}"
#         )

    # def open_product(self, product):
    #     self.page.evaluate(
    #         "el => el.scrollIntoView({block:'center'})", product
    #     )
    #     self.page.wait_for_timeout(1000)
    #     product.locator("xpath=" + self.PLP_PRODUCT_LINK).click()
    #     self.page.wait_for_timeout(3000)

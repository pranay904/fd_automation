
class PDPPage:

    def __init__(self, page):
        self.page = page

        self.pdp_metal = "//span[@id='pdp-metal']"
        self.pdp_shape = "//span[@id='pdp-shape']"
        self.pdp_style = "//span[@id='pdp-style']"
        self.pdp_carat = "//span[@id='pdp-carat']"
        self.pdp_price = "//span[contains(@class,'price')]"
        self.pdp_mrp = "//span[contains(@class,'mrp')]"

    def get_pdp_details(self):

        return {
            "metal": self.page.locator(self.pdp_metal).inner_text(),
            "shape": self.page.locator(self.pdp_shape).inner_text(),
            "style": self.page.locator(self.pdp_style).inner_text(),
            "carat": self.page.locator(self.pdp_carat).inner_text(),
            "price": self.page.locator(self.pdp_price).inner_text(),
            "mrp": self.page.locator(self.pdp_mrp).inner_text(),
        }
















# from FD.components.base_filters import BaseFilters
#
#
# class PDPValidator(BaseFilters):
#
#     # ---------------- PDP LOCATORS ----------------
#     PDP_PRICE = "//div[@class='container']//h2[1]"
#     PDP_METAL = "//div[label[text()='metal :']]/span"
#     PDP_SHAPE = "//label[contains(text(),'Diamond shape')]/following-sibling::span"
#     PDP_CARAT = "//label[contains(text(),'Diamond carat')]/following-sibling::span"
#     PDP_STYLE = "//h5[contains(@class,'title_h5')]"
#
#     All_PLP = "//*[@class='mob_mod']";
#
#     def validate_pdp(self, expected: dict, plp_price: str):
#         pdp_price = self.page.locator(self.PDP_PRICE).text_content().strip()
#         pdp_metal = self.page.locator(self.PDP_METAL).text_content().strip()
#         pdp_shape = self.page.locator(self.PDP_SHAPE).text_content().strip()
#         pdp_carat = self.page.locator(self.PDP_CARAT).text_content().strip()
#         pdp_style = self.page.locator(self.PDP_STYLE).text_content().strip()
#
#         assert self.normalize_price(plp_price.split()[0]) == \
#                self.normalize_price(pdp_price.split()[0]), "Price mismatch"
#
#         if expected.get("metal"):
#             assert self.normalize_metal(pdp_metal) == \
#                    self.normalize_metal(expected["metal"])
#
#         if expected.get("shape"):
#             assert expected["shape"].lower() in self.normalize_text(pdp_shape)
#
#         if expected.get("style"):
#             assert expected["style"].lower() in self.normalize_text(pdp_style)
#
#         if expected.get("carat"):
#             assert expected["carat"].lower() in self.normalize_text(pdp_carat)

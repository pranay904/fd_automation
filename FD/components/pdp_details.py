from FD.components.base_filters import BaseFilters


class PDPValidator(BaseFilters):

    # ---------------- PDP LOCATORS ----------------
    PDP_PRICE = "//div[@class='container']//h2[1]"
    PDP_METAL = "//div[label[text()='metal :']]/span"
    PDP_SHAPE = "//label[contains(text(),'Diamond shape')]/following-sibling::span"
    PDP_CARAT = "//label[contains(text(),'Diamond carat')]/following-sibling::span"
    PDP_STYLE = "//h5[contains(@class,'title_h5')]"

    All_PLP = "//*[@class='mob_mod']"

    def validate_pdp(self, expected: dict, plp_price: str):
        pdp_price = self.page.locator(self.PDP_PRICE).text_content().strip()
        pdp_metal = self.page.locator(self.PDP_METAL).text_content().strip()
        pdp_shape = self.page.locator(self.PDP_SHAPE).text_content().strip()
        pdp_carat = self.page.locator(self.PDP_CARAT).text_content().strip()
        pdp_style = self.page.locator(self.PDP_STYLE).text_content().strip()

        assert self.normalize_price(plp_price.split()[0]) == \
               self.normalize_price(pdp_price.split()[0]), "Price mismatch"

        if expected.get("metal"):
            assert self.normalize_metal(pdp_metal) == \
                   self.normalize_metal(expected["metal"])

        if expected.get("shape"):
            assert expected["shape"].lower() in self.normalize_text(pdp_shape)

        if expected.get("style"):
            assert expected["style"].lower() in self.normalize_text(pdp_style)

        if expected.get("carat"):
            assert expected["carat"].lower() in self.normalize_text(pdp_carat)

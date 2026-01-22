class CommonFilters:
    def __init__(self, page):
        self.page = page

    # ---------------- DROPDOWNS ----------------
    METAL_DROPDOWN = "//div[contains(text(),'metal')]"
    SHAPE_DROPDOWN = "//div[contains(text(),'shape')]"
    STYLE_DROPDOWN = "//div[contains(text(),'style')]"
    CARAT_DROPDOWN = "//div[contains(text(),'carat')]"

    # ---------------- ITEMS ----------------
    METAL_ITEMS = "//div[@class='drop_item_metal drop_item']//ul/li"
    SHAPE_ITEMS = "//div[@class='drop_item_shape drop_item']//ul/li"
    STYLE_ITEMS = "//div[@class='drop_item_style drop_item']//ul/li"
    CARAT_ITEMS = "//div[@class='drop_item_carat drop_item']//ul/li"

    FILTER_TAGS = "(//div[@class='filter_tags for_desktop'])[1]"

    # ---------------- PLP LOCATORS ----------------
    PLP_CARDS = "//div[contains(@class,'product-card')]"
    PLP_METAL = ".//span[contains(@class,'metal')]"
    PLP_SHAPE = ".//span[contains(@class,'shape')]"
    PLP_STYLE = ".//span[contains(@class,'style')]"
    PLP_CARAT = ".//span[contains(@class,'carat')]"

    # ---------------- UTILS ----------------
    def _normalize(self, text):
        return text.lower().replace(" ", "").replace("kt", "k")

    # ---------------- SELECT FILTER ----------------
    def select_filter(self, dropdown, items, expected_value):
        if not expected_value:
            print(f"Skipped filter: {expected_value}")
            return None

        self.page.locator(dropdown).click()
        options = self.page.locator(items)
        options.first.wait_for(state="visible")

        for i in range(options.count()):
            text = options.nth(i).text_content().strip()
            if self._normalize(expected_value) in self._normalize(text):
                options.nth(i).click()
                print(f" Selected filter: {text}")
                return self._normalize(text)

        print(f" Filter '{expected_value}' not available – skipped")
        return None

    # ---------------- ASSERT FILTER TAG ----------------
    def assert_filter_tag_applied(self, expected_value):
        if not expected_value:
            return

        tags = self.page.locator(self.FILTER_TAGS)
        tags.wait_for(state="visible")
        applied_tags = [self._normalize(t) for t in tags.all_text_contents()]

        if expected_value in applied_tags:
            print(f" Filter tag applied correctly: {expected_value}")
        else:
            print(f" Filter tag NOT applied: expected {expected_value}, actual {applied_tags}")

    # ---------------- ASSERT PLP ----------------
    def assert_plp_matches_filter(self, filter_type, expected_value):
        if not expected_value:
            return

        cards = self.page.locator(self.PLP_CARDS)
        count = cards.count()

        if count == 0:
            print(f" No products displayed for filter: {expected_value}")
            return

        missing_products = 0
        for i in range(count):
            card = cards.nth(i)
            if filter_type == "metal":
                actual = card.locator(self.PLP_METAL).text_content()
            elif filter_type == "shape":
                actual = card.locator(self.PLP_SHAPE).text_content()
            elif filter_type == "style":
                actual = card.locator(self.PLP_STYLE).text_content()
            elif filter_type == "carat":
                actual = card.locator(self.PLP_CARAT).text_content()
            else:
                continue

            if self._normalize(expected_value) in self._normalize(actual):
                print(f" Product {i+1} matches {filter_type}: {actual}")
            else:
                print(f" Product {i+1} does NOT match {filter_type}: {actual}")
                missing_products += 1

        if missing_products == 0:
            print(f" All PLP products match {filter_type}: {expected_value}")
        else:
            print(f"⚠ {missing_products}/{count} products do NOT match {filter_type}: {expected_value}")

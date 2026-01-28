import re
from playwright.sync_api import TimeoutError

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

    # ---------------- FILTER TAG ----------------
    FILTER_TAG_VALUE = "//div[contains(@class,'filter_tags')]//div[contains(@class,'tag_box')]/span[1]"

    # ---------------- PLP LOCATORS (from Java code) ----------------
    PLP_PRODUCTS = "//div[@class='product_box']"
    PLP_MOB_MOD = ".//*[contains(@class,'mob_mod')]//a[1]"
    PLP_PRICE = ".//h4[contains(@class,'mb-3')]"
    PLP_PRODUCT_LINK = ".//a[1]"
    PLP_ACTIVE_METAL = ".//div[contains(@class,'metal_color')]//div[contains(@class,'metal_box') and contains(@class,'active')]"

    # ---------------- PDP LOCATORS (from Java code) ----------------
    PDP_PRICE = "//div[@class='container']//h2[1]"
    PDP_METAL = "//div[label[text()='metal :']]/span"
    PDP_SHAPE = "//label[contains(text(),'Diamond shape')]/following-sibling::span"
    PDP_CARAT = "//label[contains(text(),'Diamond carat')]/following-sibling::span"
    PDP_STYLE = "//h5[contains(@class,'title_h5')]"

    # ---------------- NORMALIZERS ----------------
    def normalize_metal(self, text):
        if not text:
            return ""
        text = text.lower()
        karat_match = re.search(r'(10|14|18)\s*(k|kt)', text)
        karat = karat_match.group(1) if karat_match else ""

        if "white" in text:
            color = "White"
        elif "yellow" in text:
            color = "Yellow"
        elif "rose" in text:
            color = "Rose"
        elif "platinum" in text:
            color = "Platinum"
        else:
            color = ""

        return f"{karat}Kt {color} Gold".strip() if karat and color else text.strip()

    def normalize_text(self, text):
        return text.strip().lower() if text else ""

    def normalize_price(self, text):
        return text.replace(",", "").strip().lower()

    # ---------------- SELECT FILTER ----------------
    def apply_filter(self, dropdown, items, filter_type, expected_value):
        if not expected_value:
            return None

        self.page.locator(dropdown).click()
        options = self.page.locator(items)
        options.first.wait_for(state="visible", timeout=5000)

        for i in range(options.count()):
            text = options.nth(i).text_content().strip()

            if filter_type == "metal":
                if self.normalize_metal(expected_value) == self.normalize_metal(text):
                    options.nth(i).click()

                    # ✅ WAIT AFTER FILTER APPLIED
                    self.page.wait_for_timeout(3000)

                    selected = self.normalize_metal(text)
                    print(f"Selected filter value: {expected_value}")
                    print(f"Applied filter value:  {selected}")
                    return selected
            else:
                if expected_value.lower() in text.lower():
                    options.nth(i).click()

                    # ✅ WAIT AFTER FILTER APPLIED
                    self.page.wait_for_timeout(3000)

                    selected = text.strip()
                    print(f"Selected filter value: {expected_value}")
                    print(f"Applied filter value:  {selected}")
                    return selected

        print(f"Filter '{expected_value}' not found")
        return None

    # ---------------- ASSERT FILTER TAGS ----------------
    def assert_filter_tags(self, expected: dict):
        tags = self.page.locator(self.FILTER_TAG_VALUE)
        tags.first.wait_for(state="visible", timeout=5000)

        applied_tags = tags.all_text_contents()

        for filter_type, expected_value in expected.items():
            if filter_type == "metal":
                expected_norm = self.normalize_metal(expected_value)
                actual = [self.normalize_metal(t) for t in applied_tags]
            else:
                expected_norm = expected_value.lower()
                actual = [t.lower() for t in applied_tags]

            print(f"Expected tag value: {expected_value}")
            print(f"Applied tag value:  {actual}")

            if expected_norm not in actual:
                print(f"❌ Tag mismatch for {filter_type}: {expected_value}")
                return False

        print("✅ Tag matched")
        return True

    # ---------------- PLP -> PDP VALIDATION ----------------
    def validate_plp_pdp(self, expected: dict, product_count=5):
        products = self.page.locator(self.PLP_PRODUCTS)
        total = min(product_count, products.count())

        print(f"Total products to validate: {total}")

        expected_metal_color = ""
        if expected.get("metal"):
            expected_metal_color = expected["metal"].split()[-2].lower()

        for i in range(total):
            products = self.page.locator(self.PLP_PRODUCTS)
            product = products.nth(i)

            # PLP URL
            mob_mod = product.locator("xpath=" + self.PLP_MOB_MOD)
            mob_mod_href = mob_mod.get_attribute("href")
            print(f"\n--- PRODUCT {i + 1} ---")
            print(f"Product URL: {mob_mod_href}")

            # PLP PRICE
            plp_price = product.locator("xpath=" + self.PLP_PRICE).text_content().strip()
            print(f"PLP Price: {plp_price}")

            # PLP Active Metal class
            active_metal_class = product.locator("xpath=" + self.PLP_ACTIVE_METAL).get_attribute("class").strip()
            print(f"PLP Active Metal Class: {active_metal_class}")

            # VALIDATE ACTIVE METAL COLOR
            if expected_metal_color and expected_metal_color in active_metal_class:
                print(f"PASS: Active metal matches expected color: {expected_metal_color}")
            else:
                print(f"FAIL: Active metal mismatch. Expected: {expected_metal_color}, Actual: {active_metal_class}")
                return False

            # SCROLL + CLICK
            self.page.evaluate("element => element.scrollIntoView({behavior:'smooth', block:'center'})", product)
            self.page.wait_for_timeout(1000)

            product.locator("xpath=" + self.PLP_PRODUCT_LINK).click()
            self.page.wait_for_timeout(3000)

            # PDP VALUES
            pdp_price = self.page.locator("xpath=" + self.PDP_PRICE).text_content().strip()
            pdp_metal = self.page.locator("xpath=" + self.PDP_METAL).text_content().strip()
            pdp_shape = self.page.locator("xpath=" + self.PDP_SHAPE).text_content().strip()
            pdp_carat = self.page.locator("xpath=" + self.PDP_CARAT).text_content().strip()
            pdp_style = self.page.locator("xpath=" + self.PDP_STYLE).text_content().strip()

            print(f"PDP Price: {pdp_price}")
            print(f"PDP Metal: {pdp_metal}")
            print(f"PDP Shape: {pdp_shape}")
            print(f"PDP Carat: {pdp_carat}")
            print(f"PDP Style: {pdp_style}")

            # COMPARISONS
            if self.normalize_price(plp_price.split(" ")[0]) == self.normalize_price(pdp_price.split(" ")[0]):
                print("PASS: Price matched")
            else:
                print(f"FAIL: Price mismatch. PLP={plp_price}, PDP={pdp_price}")
                return False

            if expected.get("metal") and self.normalize_metal(pdp_metal) == self.normalize_metal(expected.get("metal")):
                print("PASS: Metal matched")
            else:
                print(f"FAIL: Metal mismatch. Expected={expected.get('metal')}, PDP={pdp_metal}")
                return False

            if expected.get("shape") and expected.get("shape").lower() in self.normalize_text(pdp_shape):
                print("PASS: Shape matched")
            else:
                print(f"FAIL: Shape mismatch. Expected={expected.get('shape')}, PDP={pdp_shape}")
                return False

            if expected.get("style") and expected.get("style").lower() in self.normalize_text(pdp_style):
                print("PASS: Style matched")
            else:
                print(f"FAIL: Style mismatch. Expected={expected.get('style')}, PDP={pdp_style}")
                return False

            if expected.get("carat") and expected.get("carat").lower() in self.normalize_text(pdp_carat):
                print("PASS: Carat matched")
            else:
                print(f"FAIL: Carat mismatch. Expected={expected.get('carat')}, PDP={pdp_carat}")
                return False

            # BACK
            self.page.go_back()
            self.page.wait_for_timeout(1500)

        print("\n✅ All products validated successfully")
        return True


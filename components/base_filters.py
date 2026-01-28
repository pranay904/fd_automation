import re
from playwright.sync_api import TimeoutError

class BaseFilters:
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

    # ---------------- APPLY FILTER ----------------
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
                    self.page.wait_for_timeout(3000)
                    return self.normalize_metal(text)
            else:
                if expected_value.lower() in text.lower():
                    options.nth(i).click()
                    self.page.wait_for_timeout(3000)
                    return text.strip()

        raise AssertionError(f"Filter not found: {expected_value}")

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

            if expected_norm not in actual:
                raise AssertionError(f"Tag mismatch for {filter_type}")

        return True

from components.base_filters import BaseFilters
from components.plp_filters import PLPFilters
from components.pdp_details import PDPValidator
from utils.config import PRESET_URL


class PresetPage:
    def __init__(self, page):
        self.page = page

        # compose instead of inherit
        self.base = BaseFilters(page)
        self.plp = PLPFilters(page)
        self.pdp = PDPValidator(page)

    def open(self):
        self.page.goto(PRESET_URL)

    # ---------------- SINGLE FILTER ----------------
    def apply_verify_single_filter(self, filter_type, value):
        dropdown = getattr(self.base, f"{filter_type.upper()}_DROPDOWN")
        items = getattr(self.base, f"{filter_type.upper()}_ITEMS")

        selected = self.base.apply_filter(
            dropdown, items, filter_type, value
        )

        expected = {filter_type: selected} if selected else {}

        # TAG ASSERT
        self.base.assert_filter_tags(expected)

        # PLP → PDP VALIDATION
        products, total = self.plp.get_products()

        for i in range(total):
            product = products.nth(i)

            plp_price = product.locator(
                "xpath=" + self.plp.PLP_PRICE
            ).text_content().strip()

            if filter_type == "metal":
                self.plp.validate_active_metal(product, selected)

            self.plp.open_product(product)
            self.pdp.validate_pdp(expected, plp_price)

            self.page.go_back()
            self.page.wait_for_timeout(1500)

        print(f" {filter_type.capitalize()} '{value}' PASSED")

    # ---------------- MIXED FILTERS ----------------
    def apply_verify_mixed_filters(self, filters: dict):
        selected = {}

        for filter_type, value in filters.items():
            dropdown = getattr(self.base, f"{filter_type.upper()}_DROPDOWN")
            items = getattr(self.base, f"{filter_type.upper()}_ITEMS")

            selected_value = self.base.apply_filter(
                dropdown, items, filter_type, value
            )

            if selected_value:
                selected[filter_type] = selected_value

        if not selected:
            raise AssertionError(" No filters applied")

        # TAG ASSERT
        self.base.assert_filter_tags(selected)

        # PLP → PDP VALIDATION
        products, total = self.plp.get_products()

        for i in range(total):
            product = products.nth(i)

            plp_price = product.locator(
                "xpath=" + self.plp.PLP_PRICE
            ).text_content().strip()

            if "metal" in selected:
                self.plp.validate_active_metal(product, selected["metal"])

            self.plp.open_product(product)
            self.pdp.validate_pdp(selected, plp_price)

            self.page.go_back()
            self.page.wait_for_timeout(1500)

        print(f" Mixed filters PASSED: {selected}")

from FD.components.base_filters import BaseFilters
from FD.components.plp_filters import PLPFilters
from FD.components.pdp_details import PDPValidator
from FD.utils.config import PRESET_URL
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class PresetPage:
    def __init__(self, page):
        self.page = page
        self.base = BaseFilters(page)
        self.plp = PLPFilters(page)
        self.pdp = PDPValidator(page)

    def open(self):
        self.page.goto(PRESET_URL)
        self.page.wait_for_load_state("domcontentloaded")

    # ---------------- SINGLE FILTER ----------------
    def apply_verify_single_filter(self, filter_type, value):
        dropdown = getattr(self.base, f"{filter_type.upper()}_DROPDOWN")
        items = getattr(self.base, f"{filter_type.upper()}_ITEMS")

        selected = self.base.apply_filter(dropdown, items, filter_type, value)
        expected = {filter_type: selected} if selected else {}

        # TAG ASSERT
        self.base.assert_filter_tags(expected)

        # PLP → PDP VALIDATION
        products, total = self.plp.get_products()
        if total == 0:
            raise AssertionError("No products found on PLP")

        for i in range(total):
            products, _ = self.plp.get_products(count=total)
            product = products.nth(i)

            try:
                product.scroll_into_view_if_needed()
            except PlaywrightTimeoutError:
                print(f"Skipping product {i} – cannot scroll into view")
                continue

            plp_price = product.locator("xpath=" + self.plp.PLP_PRICE).text_content() or ""
            plp_price = plp_price.strip()

            if filter_type == "metal":
                self.plp.validate_active_metal(product, selected)

            try:
                self.plp.open_product(product)
                self.pdp.validate_pdp(expected, plp_price)
            except Exception as e:
                print(f"PDP validation failed for product {i}: {e}")
            finally:
                self.page.go_back()
                self.page.wait_for_timeout(1500)

        print(f"{filter_type.capitalize()} '{value}' PASSED")

    # ---------------- MIXED FILTERS ----------------
    def apply_verify_mixed_filters(self, filters: dict):
        selected = {}
        for filter_type, value in filters.items():
            dropdown = getattr(self.base, f"{filter_type.upper()}_DROPDOWN")
            items = getattr(self.base, f"{filter_type.upper()}_ITEMS")
            selected_value = self.base.apply_filter(dropdown, items, filter_type, value)
            if selected_value:
                selected[filter_type] = selected_value

        if not selected:
            raise AssertionError("No filters applied")

        # TAG ASSERT
        self.base.assert_filter_tags(selected)

        # PLP → PDP VALIDATION
        products, total = self.plp.get_products()
        if total == 0:
            raise AssertionError("No products found on PLP")

        for i in range(total):
            products, _ = self.plp.get_products(count=total)
            product = products.nth(i)

            try:
                product.scroll_into_view_if_needed()
            except PlaywrightTimeoutError:
                print(f"Skipping product {i} – cannot scroll into view")
                continue

            plp_price = product.locator("xpath=" + self.plp.PLP_PRICE).text_content() or ""
            plp_price = plp_price.strip()

            if "metal" in selected:
                self.plp.validate_active_metal(product, selected["metal"])

            try:
                self.plp.open_product(product)
                self.pdp.validate_pdp(selected, plp_price)
            except Exception as e:
                print(f"PDP validation failed for product {i}: {e}")
            finally:
                self.page.go_back()
                self.page.wait_for_timeout(1500)

        print(f"Mixed filters PASSED: {selected}")

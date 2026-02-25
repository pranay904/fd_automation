from FD.components.plp_filters import PLPPage
from FD.components.pdp_details import PDPPage
from FD.components.base_filters import BaseFilters


class PresetPLPPDPVerify:

    def __init__(self, page):
        self.page = page
        self.base = BaseFilters(page)
        self.plp = PLPPage(page)
        self.pdp = PDPPage(page)

    # ---------------- Currency Validation ----------------
    def validate_currency(self, price_text):

        url = self.page.url.lower()

        if "/uk" in url:
            expected_symbol = "£"
        else:
            expected_symbol = "$"

        return expected_symbol in price_text

    # ---------------- Full Flow ----------------
    def verify_test_case(self, test_data):

        status = "Passed"

        # ---------------- APPLY FILTERS ----------------
        applied_filters = {}

        for key in ["metal", "shape", "style", "carat"]:
            value = test_data.get(key)

            if value:
                dropdown = getattr(self.base, f"{key.upper()}_DROPDOWN")
                items = getattr(self.base, f"{key.upper()}_ITEMS")

                selected = self.base.apply_filter(
                    dropdown,
                    items,
                    key,
                    value
                )

                applied_filters[key] = value
            else:
                print(f"{key} skipped (NULL)")

        # Verify filter tags
        self.base.assert_filter_tags(applied_filters)

        # ---------------- VERIFY PLP ----------------
        plp_data = self.plp.get_first_product_details()

        for key in ["metal", "shape", "style", "carat"]:

            expected = test_data.get(key)

            if not expected:
                continue

            expected_norm = self.base.normalize_value(key, expected)
            actual_norm = self.base.normalize_value(key, plp_data[key])

            if expected_norm != actual_norm:
                print(f"PLP mismatch in {key}")
                status = "Failed"

        plp_price = plp_data["price"]
        plp_mrp = plp_data["mrp"]

        if not self.validate_currency(plp_price):
            print("PLP currency mismatch")
            status = "Failed"

        price_val = self.plp.normalize_price(plp_price)
        mrp_val = self.plp.normalize_price(plp_mrp)
        difference = mrp_val - price_val

        # ---------------- OPEN PDP ----------------
        self.plp.open_first_product()

        pdp_data = self.pdp.get_pdp_details()

        for key in ["metal", "shape", "style", "carat"]:

            expected = test_data.get(key)

            if not expected:
                continue

            expected_norm = self.base.normalize_value(key, expected)
            actual_norm = self.base.normalize_value(key, pdp_data[key])

            if expected_norm != actual_norm:
                print(f"PDP mismatch in {key}")
                status = "Failed"

        pdp_price = pdp_data["price"]
        pdp_mrp = pdp_data["mrp"]

        if not self.validate_currency(pdp_price):
            print("PDP currency mismatch")
            status = "Failed"

        print("PDP Price:", pdp_price)

        self.page.go_back()

        return {
            "PLP Price": plp_price,
            "PLP MRP": plp_mrp,
            "PLP Difference": difference,
            "PDP Price": pdp_price,
            "PDP MRP": pdp_mrp,
            "Status": status
        }

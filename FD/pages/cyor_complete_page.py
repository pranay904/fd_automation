import re
from FD.pages.base_page import BasePage
from FD.utils.price_calculator import PriceCalculator


class CompletePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # -------------------- STORE COMPLETE PRODUCT DATA --------------------
        self.complete_product_data = {
            "setting_name": "",
            "setting_price": "",
            "setting_mrp": "",
            "setting_metal": "",

            "diamond_name": "",
            "diamond_price": "",
            "diamond_mrp": "",
            "diamond_carat": "",
            "diamond_shape": "",

            "total_price": "",
            "total_mrp": "",
            "saved_amount": "",

            "selected_ring_size": "",
            "estimated_delivery_date": ""
        }

    def normalize(self, text):
        return re.sub(r"\s+", " ", text).strip().lower()

    def parse_stepper(self, text):
        text = text.lower()

        name = text.split("-")[0].strip()
        price = re.search(r'\$[\d,]+', text)
        metal = re.search(r'(10kt|14kt|18kt|white|rose|yellow|gold|platinum)', text)

        return {
            "name": name,
            "price": price.group(0) if price else None,
            "metal": metal.group(0) if metal else None
        }

    # -------------------- STEPPER --------------------
    def verify_stepper(self, setting, diamond):

        print("\n===== VERIFYING STEPPER =====")

        stepper = self.page.locator("div.steps_block.for_desktop")
        stepper.wait_for(state="visible", timeout=10000)

        # ---------------- SETTING ----------------
        step1_text = stepper.locator("div.steps_box").nth(0).locator(".prod_name").inner_text()
        step1 = self.parse_stepper(step1_text)

        print("ACTUAL SETTING:", step1)
        print("EXPECTED PRICE:", setting["price"])

        assert "six prong" in step1["name"]
        assert setting["price"] in step1["price"]
        assert step1["metal"] is not None

        print("SETTING STEP MATCHED")

        self.complete_product_data["setting_name"] = step1["name"]
        self.complete_product_data["setting_price"] = step1["price"]
        self.complete_product_data["setting_metal"] = step1["metal"]

        # ---------------- DIAMOND (STEP VALIDATION ONLY) ----------------
        step2_text = stepper.locator("div.steps_box").nth(1).locator("h3").first.inner_text()
        actual_diamond = self.normalize(step2_text)

        print("ACTUAL DIAMOND STEP:", actual_diamond)

        assert "diamond" in actual_diamond

        print("DIAMOND STEP MATCHED")

    # -------------------- TOTAL PRICE --------------------
    def verify_heading_and_total_price(self, setting, diamond):

        print("\n===== VERIFYING COMPLETE PAGE PRICE =====")

        price_box = self.page.locator("div.price_box h2")
        price_box.wait_for(state="visible", timeout=10000)

        ui_price = price_box.inner_text().split()[0]
        ui_mrp = price_box.locator("span.pdp_mrp_box").inner_text().strip()

        expected_price = PriceCalculator.calculate_total_price(setting, diamond)
        expected_mrp = PriceCalculator.calculate_total_mrp(setting, diamond)

        expected_price_str = f"${int(expected_price):,}"
        expected_mrp_str = f"${int(expected_mrp):,}"

        print("ACTUAL PRICE:", ui_price, "EXPECTED:", expected_price_str)
        print("ACTUAL MRP:", ui_mrp, "EXPECTED:", expected_mrp_str)

        assert ui_price == expected_price_str
        assert ui_mrp == expected_mrp_str

        print("TOTAL PRICE MATCHED")

        self.complete_product_data["total_price"] = ui_price
        self.complete_product_data["total_mrp"] = ui_mrp

        return ui_price, ui_mrp

    # -------------------- SAVED AMOUNT --------------------
    def verify_saved_amount(self, total_price, total_mrp):

        print("\n===== VERIFYING SAVED AMOUNT =====")

        saved_locator = self.page.locator("div.coupon_box_wrapper p.text")
        saved_locator.wait_for(state="visible", timeout=10000)

        ui_text = saved_locator.inner_text().strip()
        ui_saved = re.search(r"\$[\d,]+", ui_text).group(0)

        expected_saved = PriceCalculator.calculate_saved_amount(total_price, total_mrp)
        expected_saved_str = f"${int(expected_saved):,}"

        print("ACTUAL SAVED:", ui_saved, "EXPECTED:", expected_saved_str)

        assert ui_saved == expected_saved_str

        print("SAVED AMOUNT MATCHED")

        self.complete_product_data["saved_amount"] = ui_saved

    # -------------------- SETTING SUMMARY --------------------
    def verify_setting_summary(self, setting):

        print("\n===== VERIFYING SETTING SUMMARY =====")

        box = self.page.locator("div.prod_list_box").nth(0)
        box.wait_for(state="visible", timeout=10000)

        name = box.locator("p span").inner_text().strip().lower()
        metal = box.locator("h5").first.inner_text().strip().lower()

        expected_name = setting["product_name"].split()[0].lower()
        expected_metal = setting["metal_color"]

        print("ACTUAL NAME:", name, "EXPECTED:", expected_name)
        print("ACTUAL METAL:", metal, "EXPECTED:", expected_metal)

        assert expected_name in name
        assert expected_metal in metal

        print("SETTING SUMMARY MATCHED")

        self.complete_product_data["setting_name"] = name
        self.complete_product_data["setting_metal"] = metal

    # -------------------- DIAMOND SUMMARY (FIXED) --------------------
    def verify_diamond_summary(self, diamond):

        print("\n===== VERIFYING DIAMOND SUMMARY =====")

        box = self.page.locator("div.prod_list_box").nth(1)
        box.wait_for(state="visible", timeout=10000)

        title = box.locator("p span").inner_text().strip().lower()

        print("ACTUAL:", title)
        print("EXPECTED:", "diamond")

        assert "diamond" in title

        # -------------------- EXTRACT CARAT & SHAPE --------------------
        carat_match = re.search(r"(\d+(\.\d+)?)\s*ct", title)
        shape_match = re.search(r"(oval|round|emerald|princess|pear|cushion|asscher|marquise)", title)

        carat = carat_match.group(1) if carat_match else None
        shape = shape_match.group(1) if shape_match else None

        print("EXTRACTED CARAT:", carat)
        print("EXTRACTED SHAPE:", shape)

        assert carat is not None, "Carat not found"
        assert shape is not None, "Shape not found"

        print("DIAMOND SUMMARY MATCHED")

        self.complete_product_data["diamond_name"] = title
        self.complete_product_data["diamond_price"] = diamond.get("price")
        self.complete_product_data["diamond_mrp"] = diamond.get("mrp")
        self.complete_product_data["diamond_carat"] = carat
        self.complete_product_data["diamond_shape"] = shape

    # -------------------- RING SIZE --------------------
    def select_ring_size(self):

        print("\n===== SELECTING RING SIZE =====")

        dropdown = self.page.locator("(//div[contains(@class,'current_active')])[1]")
        dropdown.scroll_into_view_if_needed()
        dropdown.click()

        dropdown_list = self.page.locator("ul.p-0:visible")
        dropdown_list.wait_for(state="visible", timeout=10000)

        options = dropdown_list.locator("li span")

        selected = options.nth(1)
        value = selected.inner_text().strip()

        selected.click()

        print("SELECTED RING SIZE:", value)

        self.complete_product_data["selected_ring_size"] = value

        return value

    # -------------------- SHIPMENT DATE --------------------
    def get_estimated_shipment(self):

        print("\n===== FETCHING SHIPMENT DATE =====")

        date = self.page.locator("span.date")
        date.wait_for(state="visible", timeout=10000)

        value = date.inner_text().strip()

        print("SHIPMENT DATE:", value)

        self.complete_product_data["estimated_delivery_date"] = value

        return value

    # -------------------- GET DATA --------------------
    def get_complete_product_data(self):

        print("\n===== COMPLETE PRODUCT DATA =====")
        print(self.complete_product_data)

        return self.complete_product_data

    # -------------------- ADD TO BAG --------------------
    def add_to_bag(self):

        print("\n===== ADD TO BAG =====")

        btn = self.page.locator("div.sticky_btns span:has-text('Add to bag')")
        btn.wait_for(state="visible", timeout=10000)

        btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        btn.click()
        self.page.wait_for_timeout(3000)

        print("Clicked Add to Bag")
import re
from FD.pages.base_page import BasePage
from FD.utils.price_calculator import PriceCalculator


class CompletePage(BasePage):

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

        # SETTING
        step1_text = stepper.locator("div.steps_box").nth(0).locator(".prod_name").inner_text()
        step1 = self.parse_stepper(step1_text)

        assert "six prong" in step1["name"]
        assert setting["price"] in step1["price"]
        assert step1["metal"] is not None

        # DIAMOND
        step2_text = stepper.locator("div.steps_box").nth(1).locator("h3").first.inner_text()
        assert "diamond" in self.normalize(step2_text)

        # COMPLETE
        step3_text = stepper.locator("div.steps_box").nth(2).locator("h3").first.inner_text()
        assert "complete" in step3_text.lower()

        print("Stepper verification PASSED")

    # -------------------- TOTAL PRICE --------------------
    def verify_heading_and_total_price(self, setting, diamond):

        print("\n===== VERIFYING COMPLETE PAGE PRICE =====")

        price_box = self.page.locator("div.price_box h2")
        price_box.wait_for(state="visible", timeout=10000)

        ui_price = price_box.inner_text().split()[0]
        ui_mrp = price_box.locator("span.pdp_mrp_box").inner_text().strip()

        print("UI Total Price :", ui_price)
        print("UI Total MRP   :", ui_mrp)

        expected_price = PriceCalculator.calculate_total_price(setting, diamond)
        expected_mrp = PriceCalculator.calculate_total_mrp(setting, diamond)

        expected_price_str = f"${int(expected_price):,}"
        expected_mrp_str = f"${int(expected_mrp):,}"

        print("Expected Price :", expected_price_str)
        print("Expected MRP   :", expected_mrp_str)

        assert ui_price == expected_price_str, f"Price mismatch: UI={ui_price}, Expected={expected_price_str}"
        assert ui_mrp == expected_mrp_str, f"MRP mismatch: UI={ui_mrp}, Expected={expected_mrp_str}"

        print("Total Price & MRP MATCHED")

        return ui_price, ui_mrp

    # -------------------- SAVED AMOUNT --------------------
    def verify_saved_amount(self, total_price, total_mrp):

        print("\n===== VERIFYING SAVED AMOUNT =====")

        saved_locator = self.page.locator("div.coupon_box_wrapper p.text")
        saved_locator.wait_for(state="visible", timeout=10000)

        ui_text = saved_locator.inner_text().strip()
        ui_saved = re.search(r"\$[\d,]+", ui_text).group(0)

        print("UI Saved:", ui_saved)

        expected_saved = PriceCalculator.calculate_saved_amount(total_price, total_mrp)
        expected_saved_str = f"${int(expected_saved):,}"

        print("Expected:", expected_saved_str)

        assert ui_saved == expected_saved_str, f"Saved mismatch: UI={ui_saved}, Expected={expected_saved_str}"

        print("Saved Amount MATCHED")

    # -------------------- SETTING SUMMARY --------------------
    def verify_setting_summary(self, setting):

        print("\n===== VERIFYING SETTING SUMMARY =====")

        box = self.page.locator("div.prod_list_box").nth(0)
        box.wait_for(state="visible", timeout=10000)

        name = box.locator("p span").inner_text().strip().lower()
        metal = box.locator("h5").first.inner_text().strip().lower()

        print("UI Name  :", name)
        print("UI Metal :", metal)

        assert setting["product_name"].split()[0].lower() in name
        assert setting["metal_color"] in metal

        print("Setting summary MATCHED")

    # -------------------- DIAMOND SUMMARY --------------------
    def verify_diamond_summary(self, diamond):

        print("\n===== VERIFYING DIAMOND SUMMARY =====")

        box = self.page.locator("div.prod_list_box").nth(1)
        box.wait_for(state="visible", timeout=10000)

        title = box.locator("p span").inner_text().strip().lower()

        print("UI Title:", title)

        assert "diamond" in title

        print("Diamond summary MATCHED")

    # -------------------- RING SIZE --------------------
    def select_ring_size(self):
        print("\n===== SELECTING RING SIZE =====")

        # 1️⃣ Click dropdown (active ring size)
        dropdown = self.page.locator("(//div[contains(@class,'current_active')])[1]")
        dropdown.scroll_into_view_if_needed()
        dropdown.click()

        # 2️⃣ Wait for visible dropdown (IMPORTANT)
        dropdown_list = self.page.locator("ul.p-0:visible")
        dropdown_list.wait_for(state="visible", timeout=10000)

        # 3️⃣ Get visible options ONLY
        options = dropdown_list.locator("li span")

        count = options.count()
        print(f"Total visible options: {count}")

        assert count > 1, "No ring size options visible"

        # 4️⃣ Select 2nd option (stable)
        selected = options.nth(1)
        value = selected.inner_text().strip()

        selected.scroll_into_view_if_needed()
        selected.click()

        print(f"Selected Ring Size: {value}")

        return value

    # -------------------- SHIPMENT DATE --------------------
    def get_estimated_shipment(self):

        print("\n===== FETCHING SHIPMENT DATE =====")

        date = self.page.locator("span.date")
        date.wait_for(state="visible", timeout=10000)

        value = date.inner_text().strip()

        print("Shipment:", value)

        assert value != ""

        return value

    # -------------------- ADD TO BAG --------------------
    def add_to_bag(self):

        print("\n===== ADD TO BAG =====")

        btn = self.page.locator("div.sticky_btns span:has-text('Add to bag')")
        btn.wait_for(state="visible", timeout=10000)

        btn.click()

        print("Clicked Add to Bag")
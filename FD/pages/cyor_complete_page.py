from FD.pages.base_page import BasePage
import re
import time

class CompletePage(BasePage):

    # ---------- HELPERS ----------
    def normalize(self, text):
        """
        Normalize the text to avoid mismatch due to invisible characters or inconsistent formatting.
        """
        return re.sub(r"\s+", " ", text).strip().lower()

    def money_to_int(self, value):
        """
        Convert the monetary value (e.g., "$1,000") to an integer (e.g., 1000).
        """
        return int(value.replace("$", "").replace(",", "").strip())

    def parse_4cs(self, text):
        """
        Parse the 4Cs (color, clarity, cut) from the text (e.g., "Color : D | Clarity : VVS2 | Cut : Excellent").
        """
        parts = [p.strip() for p in text.split("|")]
        color = parts[0].replace("Color :", "").strip()
        clarity = parts[1].replace("Clarity :", "").strip()
        cut = parts[2].replace("Cut :", "").strip()
        return color, clarity, cut

    # ---------- 1️ STEPPER ----------
    def verify_stepper(self, setting, diamond):
        print("\n===== VERIFYING STEPPER =====")

        # Locate the stepper block (which contains the steps)
        stepper = self.page.locator("div.steps_block.for_desktop")
        stepper.wait_for(state="visible", timeout=10000)

        # STEP 1 – SETTING
        step1 = stepper.locator("div.steps_box").nth(0)
        step1_text = step1.locator(".prod_name").inner_text()
        print("Stepper Setting:", step1_text)

        # Normalized text comparison
        normalized_step1_text = self.normalize(step1_text)
        normalized_product_name = self.normalize(setting["product_name"])

        # Print both expected and actual values for comparison
        print(f"Expected Product Name: '{setting['product_name']}'")
        print(f"Actual Stepper Product Name: '{step1_text}'")
        print(f"Normalized Expected Product Name: '{normalized_product_name}'")
        print(f"Normalized Actual Stepper Product Name: '{normalized_step1_text}'")

        # Perform the assertion with normalized values
        assert normalized_product_name in normalized_step1_text, \
            f"Product name mismatch. Expected: '{setting['product_name']}', Found: '{step1_text}'"

        assert setting["price"] in step1_text

        # STEP 2 – DIAMOND
        step2 = stepper.locator("div.steps_box").nth(1)
        step2_text = step2.locator(".prod_name").inner_text()
        print("Stepper Diamond:", step2_text)

        # Normalized text comparison for diamond
        normalized_step2_text = self.normalize(step2_text)
        normalized_diamond_title = self.normalize(diamond["title"])

        # Print both expected and actual values for comparison
        print(f"Expected Diamond Title: '{diamond['title']}'")
        print(f"Actual Stepper Diamond Title: '{step2_text}'")
        print(f"Normalized Expected Diamond Title: '{normalized_diamond_title}'")
        print(f"Normalized Actual Stepper Diamond Title: '{normalized_step2_text}'")

        assert "diamond" in self.normalize(step2.locator("h3").inner_text())
        assert diamond["price"] in step2_text

        # STEP 3 – COMPLETE
        step3 = stepper.locator("div.steps_box").nth(2)
        assert "complete" in self.normalize(step3.locator("h3").inner_text())

        print("Stepper verification PASSED")

    # ---------- 2️ H1 + TOTAL PRICE ----------
    def verify_heading_and_total_price(self, setting, diamond):
        print("\n===== VERIFYING HEADING & TOTAL PRICE =====")

        h1 = self.page.locator("h1.font-active")
        h1.wait_for(state="visible", timeout=10000)
        heading = h1.inner_text()
        print("Complete H1:", heading)

        assert self.normalize(setting["product_name"]) in self.normalize(heading)

        price_box = self.page.locator("div.price_box h2").inner_text()
        print("Complete price box:", price_box)

        expected_price = self.money_to_int(setting["price"]) + self.money_to_int(diamond["price"])
        expected_mrp = self.money_to_int(setting["mrp"]) + self.money_to_int(diamond["mrp"])

        actual_price = self.money_to_int(price_box.split()[0])
        actual_mrp = self.money_to_int(price_box.split()[-1])

        assert expected_price == actual_price
        assert expected_mrp == actual_mrp

        print(f"Total Price MATCHED: ${actual_price}")
        print(f"Total MRP MATCHED: ${actual_mrp}")

        return expected_price, expected_mrp

    # ---------- 3️ SAVED AMOUNT ----------
    def verify_saved_amount(self, total_price, total_mrp):
        print("\n===== VERIFYING SAVED AMOUNT =====")

        saved_expected = total_mrp - total_price
        saved_text = self.page.locator("div.d-flex.align-items-center p").inner_text()
        print("Saved text:", saved_text)

        assert str(saved_expected) in saved_text
        print(f"Saved amount MATCHED: ${saved_expected}")

    # ---------- 4️ SETTING SUMMARY ----------
    def verify_setting_summary(self, setting):
        print("\n===== VERIFYING SETTING SUMMARY =====")

        block = self.page.locator("div.prod_list_box").nth(0)
        text = block.inner_text()

        assert setting["product_name"] in text
        assert setting["price"] in text
        assert setting["mrp"] in text

        print("Setting summary MATCHED")

    # ---------- 5️ DIAMOND SUMMARY ----------
    def verify_diamond_summary(self, diamond):
        print("\n===== VERIFYING DIAMOND SUMMARY =====")

        block = self.page.locator("div.prod_list_box").nth(1)
        text = block.inner_text()

        exp_color, exp_clarity, exp_cut = self.parse_4cs(diamond["four_cs"])

        assert exp_color in text
        assert exp_clarity in text
        assert exp_cut.lower() in text.lower()

        assert diamond["price"] in text
        assert diamond["mrp"] in text

        print("Diamond summary MATCHED")

    # ---------- 6️ RING SIZE ----------
    def select_ring_size(self):
        print("\n===== SELECTING RING SIZE =====")

        dropdown = self.page.locator("div.drop_block")
        dropdown.click()

        size = dropdown.locator("li").nth(5).inner_text()
        dropdown.locator("li").nth(5).click()

        print("Selected ring size:", size)
        return size

    # ---------- 7️ SHIPMENT DATE ----------
    def get_estimated_shipment(self):
        shipment = self.page.locator("text=Estimated").inner_text()
        print("Estimated shipment:", shipment)
        return shipment

    # ---------- 8️ ADD TO BAG ----------
    def add_to_bag(self):
        print("\n===== ADD TO BAG =====")
        self.page.locator("text=Add to bag").click()
        print("Clicked Add to bag")

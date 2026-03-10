import time

from FD.pages.base_page import BasePage

class DiamondDetailsPage(BasePage):

    def verify_diamond_details(self, expected_details: dict):
        """Verify the price, carat, title, and 4Cs of the diamond with per-field match flags."""

        # ---------------- PRICE & MRP ----------------
        price_locator = self.page.locator("div.price_box.mt-4 h2")
        price_locator.wait_for(state="visible", timeout=10000)
        price_text = price_locator.inner_text().strip()
        print("Diamond details_page Price text:", price_text)

        parts = price_text.split()
        price = parts[0] if len(parts) > 0 else "Not found"
        mrp = parts[1] if len(parts) > 1 else "Not found"
        print(f"Diamonds_Details_Price: {price}, Diamonds_Details_MRP: {mrp}")

        # ---------------- TITLE ----------------
        title_locator = self.page.locator(".font-active.mb-3")
        title_locator.wait_for(state="visible", timeout=10000)
        actual_title = title_locator.inner_text().strip()
        print("Diamonds_Details_Title:", actual_title)
        actual_title_clean = actual_title.replace("Lab Grown", "").strip()

        # ---------------- 4Cs ----------------
        four_cs_locator = self.page.locator("div.diam_detail.mb-3 p:nth-child(1)")
        four_cs_locator.wait_for(state="visible", timeout=10000)
        four_cs_text = four_cs_locator.inner_text().strip()
        print("Diamonds_Details_4Cs text:", four_cs_text)

        # ----------- FLEXIBLE 4Cs PARSING -----------
        def parse_4cs(text):
            """Parse 4Cs text and return only first 3: color, clarity, cut"""
            parts = [p.strip() for p in text.split("|")]
            # Handle labeled format: "Color : D", "Clarity : VVS2", "Cut : Excellent"
            color = parts[0].replace("Color :", "").strip()
            clarity = parts[1].replace("Clarity :", "").strip()
            cut = parts[2].replace("Cut :", "").strip()
            return color, clarity, cut

        details_color, details_clarity, details_cut = parse_4cs(four_cs_text)
        expected_color, expected_clarity, expected_cut = parse_4cs(expected_details["four_cs"])

        # ---------------- ONLY FIRST THREE VALUES ----------------
        color_matched = details_color == expected_color
        clarity_matched = details_clarity == expected_clarity
        cut_matched = details_cut.upper().startswith(expected_cut.upper()) if expected_cut.upper() == "EX" else details_cut.upper() == expected_cut.upper()

        # ---------------- FIELD-WISE VALIDATION ----------------
        price_matched = expected_details["price"] == price
        mrp_matched = expected_details["mrp"] == mrp
        title_matched = expected_details["title"] == actual_title_clean

        # Print per-field match/mismatch
        print(f"Price: {'MATCHED' if price_matched else f'MISMATCHED (Expected {expected_details['price']}, Found {price})'}")
        print(f"MRP: {'MATCHED' if mrp_matched else f'MISMATCHED (Expected {expected_details['mrp']}, Found {mrp})'}")
        print(f"Title: {'MATCHED' if title_matched else f'MISMATCHED (Expected {expected_details['title']}, Found {actual_title})'}")
        print(f"Color: {'MATCHED' if color_matched else f'MISMATCHED (Expected {expected_color}, Found {details_color})'}")
        print(f"Clarity: {'MATCHED' if clarity_matched else f'MISMATCHED (Expected {expected_clarity}, Found {details_clarity})'}")
        print(f"Cut: {'MATCHED' if cut_matched else f'MISMATCHED (Expected {expected_cut}, Found {details_cut})'}")

        # ---------------- FINAL TAG ----------------
        if all([price_matched, mrp_matched, title_matched, color_matched, clarity_matched, cut_matched]):
            print("Diamond validation PASSED: PLP and Details page MATCHED (with rules applied).")
            return True  # All fields matched
        else:
            print("Diamond validation FAILED: PLP and Details page MISMATCHED (check above details).")
            return False  # Some fields mismatched

    def add_diamond_to_ring(self):
        """Click on the 'Add Diamond to Ring' button."""
        add_button = self.page.locator("//span[normalize-space()='add diamond to ring']")
        add_button.wait_for(state="visible", timeout=10000)
        add_button.scroll_into_view_if_needed()
        print("Clicking 'Add Diamond to Ring' button...")
        add_button.click()
        time.sleep(10)



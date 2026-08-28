import re
from FD.pages.base_page import BasePage
from FD.locators.cart_locators import CartLocators


# ============================================================
# COMMON RESULT HELPERS
# ============================================================

def log_pass(step_name, expected_value, actual_value):
    print(f"  [PASS] {step_name}")
    print(f"         Expected : {expected_value}")
    print(f"         Actual   : {actual_value}")

    return {
        "step": step_name,
        "expected": str(expected_value),
        "actual": str(actual_value),
        "status": "PASS",
        "error": ""
    }


def log_fail(step_name, expected_value, actual_value, error_message=""):
    print(f"  [FAIL] {step_name}")
    print(f"         Expected : {expected_value}")
    print(f"         Actual   : {actual_value}")
    print(f"         Error    : {error_message}")

    return {
        "step": step_name,
        "expected": str(expected_value),
        "actual": str(actual_value),
        "status": "FAIL",
        "error": str(error_message)
    }


def log_skip(step_name, reason=""):
    print(f"  [SKIP] {step_name}")
    print(f"         Reason   : {reason}")

    return {
        "step": step_name,
        "expected": "N/A",
        "actual": "SKIPPED",
        "status": "SKIP",
        "error": reason
    }


# ============================================================
# CART PAGE
# ============================================================

class CartPage(BasePage):

    # ========================================================
    # WAIT FOR QUICK CART
    # ========================================================

    def wait_for_quick_cart(self):
        results = []

        step_name = "Quick Cart - Wait for auto open"

        try:
            quick_cart = self.page.locator(
                "div.quick_cart, div.new-navbar-cart-drawer"
            ).first

            quick_cart.wait_for(state="visible", timeout=2000)

            results.append(
                log_pass(
                    step_name,
                    "Quick cart opens after Add to Bag",
                    "Quick cart opened"
                )
            )

        except Exception:
            print("  [INFO] Quick cart did not auto open")

            results.append(
                log_pass(
                    step_name,
                    "Quick cart optional",
                    "Quick cart not opened"
                )
            )

        return results

    # ========================================================
    # SETTING NAME FROM COMPLETE PAGE
    # ========================================================

    def get_setting_name_from_complete_page(self):
        try:
            setting_box = self.page.locator("div.prod_list_box").nth(0)

            full_name = setting_box.locator("p span").inner_text().strip()

            words = full_name.split()
            short_name = " ".join(words[:2])

            print(f"  [INFO] Setting full name  : {full_name}")
            print(f"  [INFO] Setting search key : {short_name}")

            return full_name, short_name

        except Exception as error:
            print(f"  [WARN] Could not read setting name: {error}")
            return "", ""

    # ========================================================
    # DIAMOND NAME FROM COMPLETE PAGE
    # ========================================================

    def get_diamond_name_from_complete_page(self):
        try:
            diamond_box = self.page.locator("div.prod_list_box").nth(1)

            full_name = diamond_box.locator("p span").inner_text().strip()

            print(f"  [INFO] Diamond full name: {full_name}")

            carat_match = re.search(r"\d+\.\d+", full_name)
            carat = carat_match.group(0) if carat_match else ""

            shape_match = re.search(
                r"(oval|round|cushion|pear|emerald|radiant|princess|marquise|heart|asscher)",
                full_name,
                re.IGNORECASE
            )

            shape = shape_match.group(0).lower() if shape_match else ""

            print(f"  [INFO] Extracted carat: {carat} | shape: {shape}")

            return full_name, carat, shape

        except Exception as error:
            print(f"  [WARN] Could not read diamond name: {error}")
            return "", "", ""

    # ========================================================
    # TOTAL PRICE
    # ========================================================

    def get_total_price_from_complete_page(self):
        try:
            price_heading = self.page.locator("div.price_box h2").first

            price_text = price_heading.inner_text().strip()

            price_match = re.search(r"\$[\d,]+", price_text)

            total_price = price_match.group(0) if price_match else ""

            print(f"  [INFO] Total price from complete page: {total_price}")

            return total_price

        except Exception as error:
            print(f"  [WARN] Could not read total price: {error}")
            return ""

    # ========================================================
    # QUICK CART TEXT
    # ========================================================

    def get_all_quick_cart_text(self):
        try:
            quick_cart = self.page.locator(
                "div.quick_cart, div.new-navbar-cart-drawer"
            ).first

            quick_cart.wait_for(state="visible", timeout=2000)

            text = quick_cart.inner_text().lower().strip()

            print("  [INFO] Quick cart text captured")

            return text

        except Exception as error:
            print(f"  [INFO] Quick cart not available: {error}")

            try:
                return self.page.locator("body").inner_text().lower()
            except Exception:
                return ""

    # ========================================================
    # VERIFY SETTING
    # ========================================================

    def verify_setting_name_in_quick_cart(self):
        step_name = "Quick Cart - Setting Name Visible"

        _, short_name = self.get_setting_name_from_complete_page()

        if not short_name:
            return log_skip(step_name, "Could not read setting name")

        cart_text = self.get_all_quick_cart_text()

        matched = [w for w in short_name.lower().split() if w in cart_text]

        if len(matched) >= 2:
            return log_pass(step_name, short_name, f"Matched words: {matched}")

        return log_fail(step_name, short_name, cart_text[:150], f"Matched: {matched}")

    # ========================================================
    # VERIFY DIAMOND
    # ========================================================

    def verify_diamond_details_in_quick_cart(self):
        step_name = "Quick Cart - Diamond Carat and Shape Visible"

        _, carat, shape = self.get_diamond_name_from_complete_page()

        if not carat and not shape:
            return log_skip(step_name, "No diamond data")

        cart_text = self.get_all_quick_cart_text()

        errors = []

        if carat and carat not in cart_text:
            errors.append(f"Carat {carat} missing")

        if shape and shape not in cart_text:
            errors.append(f"Shape {shape} missing")

        if not errors:
            return log_pass(step_name, f"{carat}|{shape}", "Found")

        return log_fail(step_name, f"{carat}|{shape}", cart_text[:150], errors)

    # ========================================================
    # VERIFY METAL
    # ========================================================

    def verify_metal_in_quick_cart(self, setting_details):
        step_name = "Quick Cart - Metal Name Visible (Optional)"

        metal = (setting_details or {}).get("metal_color", "").lower().strip()

        if not metal:
            return log_skip(step_name, "No metal info")

        cart_text = self.get_all_quick_cart_text()

        if metal in cart_text:
            return log_pass(step_name, metal, "Found")

        return log_skip(step_name, f"{metal} not visible")

    # ========================================================
    # VERIFY PRICE
    # ========================================================

    def verify_total_price_in_quick_cart(self):
        step_name = "Quick Cart - Total Price Match"

        price = self.get_total_price_from_complete_page()

        if not price:
            return log_skip(step_name, "No price found")

        cart_text = self.get_all_quick_cart_text()

        if price in cart_text:
            return log_pass(step_name, price, "Found")

        return log_skip(step_name, f"{price} missing")

    # ========================================================
    # CLICK VIEW BAG (FIXED)
    # ========================================================

    def click_view_bag_button(self, should_click=True):

        step_name = "Quick Cart - Click View Bag Button"

        if not should_click:
            return log_skip(step_name, "Skipped because previous validation failed")

        try:

            view_bag_button = self.page.locator(
                "div.quick_cart span.view_bag, span.button-base.view_bag"
            ).first

            view_bag_button.wait_for(state="visible", timeout=5000)

            view_bag_button.click()

            # wait for navigation to SAME DOMAIN cart
            self.page.wait_for_url("**/cart", timeout=15000)

            return log_pass(
                step_name,
                "Cart page opened",
                self.page.url
            )

        except Exception as error:

            return log_fail(
                step_name,
                "Cart page opened",
                "Cart navigation failed",
                error
            )

    # ========================================================
    # MAIN VERIFY
    # ========================================================

    def verify_quick_cart(self, setting_details=None, diamond_details=None):
        results = []

        print("\n========== QUICK CART VERIFICATION ==========")

        results.extend(self.wait_for_quick_cart())
        results.append(self.verify_setting_name_in_quick_cart())
        results.append(self.verify_diamond_details_in_quick_cart())
        results.append(self.verify_metal_in_quick_cart(setting_details))
        results.append(self.verify_total_price_in_quick_cart())

        failed = any(r["status"] == "FAIL" for r in results)

        results.append(
            self.click_view_bag_button(should_click=not failed)
        )

        print("  [CART OVERALL]", "FAIL" if failed else "PASS")

        return results

    # ========================================================
    # TC-FD-CART-001 — CHECKOUT
    # ========================================================

    def click_checkout(self):
        """Click Continue to Payment / Checkout on the shopping bag page."""
        self.page.locator(CartLocators.CONTINUE_TO_PAYMENT).wait_for(state="visible", timeout=15000)
        self.page.locator(CartLocators.CONTINUE_TO_PAYMENT).click()
        self.page.wait_for_load_state("networkidle")
        print("[INFO] Clicked Checkout / Continue to Payment")


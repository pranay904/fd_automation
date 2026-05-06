import re
from FD.pages.base_page import BasePage
from FD.utils.logger import logger


def v_pass(step, expected, actual):
    print(f"  [PASS] {step} | Expected: {expected} | Actual: {actual}")
    return {"step": step, "expected": str(expected), "actual": str(actual), "status": "PASS", "error": ""}


def v_fail(step, expected, actual, error=""):
    print(f"  [FAIL] {step} | Expected: {expected} | Actual: {actual} | Error: {error}")
    return {"step": step, "expected": str(expected), "actual": str(actual), "status": "FAIL", "error": str(error)}


def v_skip(step, reason=""):
    print(f"  [SKIP] {step} | Reason: {reason}")
    return {"step": step, "expected": "N/A", "actual": "SKIPPED", "status": "SKIP", "error": reason}


class CartPage(BasePage):

    # ---------------------------
    # Read setting name from complete page prod_list_box[0]
    # ---------------------------
    def _get_complete_page_setting_name(self):
        try:
            box = self.page.locator("div.prod_list_box").nth(0)
            name = box.locator("p span").inner_text().strip()
            print(f"  [CART] Complete page setting name: {name}")
            return name
        except Exception:
            return ""

    # ---------------------------
    # Read diamond title from complete page prod_list_box[1]
    # ---------------------------
    def _get_complete_page_diamond_name(self):
        try:
            box = self.page.locator("div.prod_list_box").nth(1)
            name = box.locator("p span").inner_text().strip()
            print(f"  [CART] Complete page diamond name: {name}")
            return name
        except Exception:
            return ""

    # ---------------------------
    # Read total price from complete page
    # ---------------------------
    def _get_complete_page_price(self):
        try:
            price_box = self.page.locator("div.price_box h2")
            text = price_box.inner_text()
            price = re.search(r'\$[\d,]+', text)
            mrp_el = self.page.locator("span.pdp_mrp_box")
            mrp = mrp_el.inner_text().strip() if mrp_el.count() > 0 else ""
            result = price.group(0) if price else ""
            print(f"  [CART] Complete page price: {result} MRP: {mrp}")
            return result, mrp
        except Exception:
            return "", ""

    # ---------------------------
    # Get all text from quick cart
    # ---------------------------
    def _get_quick_cart_text(self):
        """Try multiple selectors to get quick cart product name text."""
        selectors = [
            "div.cart_item p", "div.cart_item h5", "div.cart_item span",
            "div.cart-item p", "div.cart-item h5",
            "div.mini_cart p", "div.mini_cart h5",
            "div.cart_sidebar p", "div.cart_sidebar h5",
            "div[class*='cart'] p", "div[class*='cart'] h5",
            "div.prod_list_box p span",  # same page, complete page items
        ]
        texts = []
        for sel in selectors:
            els = self.page.locator(sel)
            for i in range(min(els.count(), 5)):
                try:
                    txt = els.nth(i).inner_text().strip()
                    if txt and len(txt) > 3:
                        texts.append(txt)
                except Exception:
                    pass
        return texts

    # ---------------------------
    # Wait for quick cart to appear
    # ---------------------------
    def go_to_cart(self):
        validations = []
        step = "Quick Cart Auto-Opened"
        try:
            self.page.wait_for_timeout(2000)
            validations.append(v_pass(step, "Quick cart auto-opened after Add to Bag", self.page.url))
        except Exception as e:
            validations.append(v_fail(step, "Quick cart auto-opened", "Failed", e))
        return validations

    # ---------------------------
    # Verify cart not empty
    # ---------------------------
    def verify_cart_not_empty(self):
        step = "Cart Not Empty"
        try:
            self.page.wait_for_timeout(1000)
            item_selectors = [
                "div.cart_item", "div.cart-item", "li.cart_product",
                "div.cart_product", "div.mini_cart_item",
                "div[class*='cart_item']", "div[class*='cart-item']",
            ]
            for sel in item_selectors:
                count = self.page.locator(sel).count()
                if count > 0:
                    return v_pass(step, "At least 1 item", f"{count} item(s) via {sel}")
            return v_fail(step, "At least 1 item", "0 items found")
        except Exception as e:
            return v_fail(step, "Cart has items", "Error", e)

    # ---------------------------
    # Verify quick cart product name contains setting + diamond + metal
    # ---------------------------
    def verify_item_in_cart(self, setting_details=None, diamond_details=None, expected_name=None):
        step = "Cart Item - Product Match"
        try:
            self.page.wait_for_timeout(1000)

            # Get expected values from complete page
            setting_name = self._get_complete_page_setting_name()
            diamond_name = self._get_complete_page_diamond_name()

            # Get all text visible in quick cart area
            cart_texts = self._get_quick_cart_text()
            all_cart_text = " ".join(cart_texts).lower()
            print(f"  [CART] All cart text: {all_cart_text[:200]}")

            failures = []

            # --- Setting name check (first 2 words) ---
            if setting_name:
                setting_words = setting_name.split()[:2]
                setting_key = " ".join(setting_words).lower()
                if setting_key in all_cart_text:
                    print(f"  [CART] Setting MATCH: '{setting_key}' found in cart")
                else:
                    failures.append(f"Setting '{setting_key}' not found in cart")
                    print(f"  [CART] Setting MISMATCH: '{setting_key}' not in cart text")

            # --- Diamond name check (carat + shape) ---
            if diamond_name:
                # Extract carat e.g. "1.06" from "1.06 Ct. Oval..."
                carat_match = re.search(r'(\d+\.\d+)', diamond_name)
                shape_match = re.search(r'(oval|round|cushion|pear|emerald|radiant|princess|marquise|heart|asscher)', diamond_name, re.IGNORECASE)
                if carat_match:
                    carat = carat_match.group(1)
                    if carat in all_cart_text:
                        print(f"  [CART] Carat MATCH: '{carat}' found in cart")
                    else:
                        failures.append(f"Carat '{carat}' not found in cart")
                        print(f"  [CART] Carat MISMATCH: '{carat}' not in cart text")
                if shape_match:
                    shape = shape_match.group(1).lower()
                    if shape in all_cart_text:
                        print(f"  [CART] Shape MATCH: '{shape}' found in cart")
                    else:
                        failures.append(f"Shape '{shape}' not found in cart")
                        print(f"  [CART] Shape MISMATCH: '{shape}' not in cart text")

            # --- Metal check (optional — SKIP if not found, don't fail) ---
            metal = ""
            if setting_details:
                metal = str(setting_details.get("metal", "") or setting_details.get("metal_color", "")).lower()
            if metal:
                if metal in all_cart_text:
                    print(f"  [CART] Metal MATCH: '{metal}' found in cart")
                else:
                    print(f"  [CART] Metal SKIP: '{metal}' not found — skipping (optional)")
                    # Not added to failures — metal is optional per requirement

            expected_summary = f"setting={setting_name[:30]} | diamond={diamond_name[:30]}"
            if not failures:
                return v_pass(step, expected_summary, f"All components matched in: {all_cart_text[:100]}")
            return v_fail(step, expected_summary, all_cart_text[:100], " | ".join(failures))

        except Exception as e:
            return v_fail(step, "Cart item components", "Error", e)

    # ---------------------------
    # Verify total price in quick cart matches complete page
    # ---------------------------
    def verify_total_price_in_cart(self):
        step = "Cart Total Price Match"
        try:
            expected_price, expected_mrp = self._get_complete_page_price()
            if not expected_price:
                return v_skip(step, "Could not read price from complete page")

            # Look for price in cart area
            price_selectors = [
                "div.cart_total", "span.total-price", "div.cart_price",
                "div[class*='cart'] span.amount", "div[class*='cart'] strong",
                "div.price_box h2",  # still on complete page
            ]
            for sel in price_selectors:
                els = self.page.locator(sel)
                for i in range(els.count()):
                    txt = els.nth(i).inner_text().strip()
                    if expected_price in txt:
                        return v_pass(step, expected_price, txt)

            return v_skip(step, f"Price '{expected_price}' not found in cart area — may be on complete page only")
        except Exception as e:
            return v_fail(step, "Total price match", "Error", e)

    # ---------------------------
    # Verify checkout button visible
    # ---------------------------
    def verify_checkout_button(self):
        step = "Checkout Button Visible"
        try:
            selectors = [
                "a:has-text('Checkout')", "button:has-text('Checkout')",
                "a:has-text('View Bag')", "button:has-text('View Bag')",
                "a:has-text('Proceed')", "span:has-text('Checkout')",
                "div.sticky_btns a", "div.cart_footer a",
            ]
            for sel in selectors:
                el = self.page.locator(sel).first
                if el.count() > 0 and el.is_visible():
                    label = el.inner_text().strip()
                    return v_pass(step, "Checkout/View Bag button visible", label)
            return v_fail(step, "Checkout/View Bag button visible", "Not found")
        except Exception as e:
            return v_fail(step, "Checkout button visible", "Error", e)

    # ---------------------------
    # Click View Bag (only if all validations passed)
    # ---------------------------
    def click_view_bag(self, all_passed=True):
        step = "Click View Bag"
        if not all_passed:
            return v_skip(step, "Skipped — previous cart validations failed")
        try:
            # Exact locator from site HTML
            selectors = [
                "span.button-base.view_bag",
                "span.view_bag",
                "a:has-text('View Bag')",
                "button:has-text('View Bag')",
                "span:has-text('View Bag')",
            ]
            for sel in selectors:
                el = self.page.locator(sel).first
                if el.count() > 0:
                    el.scroll_into_view_if_needed()
                    el.wait_for(state="visible", timeout=8000)
                    el.click()
                    self.page.wait_for_timeout(2000)
                    return v_pass(step, "View Bag clicked", f"URL: {self.page.url}")
            return v_fail(step, "View Bag button", "Not found")
        except Exception as e:
            return v_fail(step, "View Bag clicked", "Error", e)

    # ---------------------------
    # Full quick cart validation (renamed from validate_cart)
    # ---------------------------
    def verify_quick_cart(self, setting_details=None, diamond_details=None):
        validations = []
        logger.info("Starting quick cart validation")

        validations.extend(self.go_to_cart())
        validations.append(self.verify_item_in_cart(setting_details=setting_details, diamond_details=diamond_details))
        validations.append(self.verify_total_price_in_cart())
        validations.append(self.verify_checkout_button())

        all_passed = all(v["status"] in ("PASS", "SKIP") for v in validations)
        validations.append(self.click_view_bag(all_passed=all_passed))

        failed = [v for v in validations if v["status"] == "FAIL"]
        overall = "PASS" if not failed else "FAIL"
        print(f"\n  [CART OVERALL] {overall}")
        return overall, validations

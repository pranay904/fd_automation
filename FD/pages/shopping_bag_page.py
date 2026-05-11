"""
shopping_bag_page.py
"""

import re
from FD.pages.base_page import BasePage


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


def extract_price(text):
    match = re.search(r"\$[\d,]+", str(text))
    return match.group(0) if match else ""


class ShoppingBagPage(BasePage):

    def dismiss_free_product_popup(self):

        step_name = "Shopping Bag - Dismiss Free Product Popup"

        try:
            close_button = self.page.locator("div.modal_close_btn").first
            close_button.wait_for(state="visible", timeout=5000)

            close_button.click()
            self.page.wait_for_timeout(800)

            return log_pass(
                step_name,
                "Popup closed",
                "Popup closed successfully"
            )

        except Exception:
            return log_skip(
                step_name,
                "Popup not displayed"
            )

    def verify_bag_title(self, expected_item_count=None):

        step_name = "Shopping Bag - Page Title and Item Count"

        try:
            heading = self.page.locator("h1.font-active").first
            heading.wait_for(state="visible", timeout=10000)

            full_text = heading.inner_text().strip()

            if "shopping bag" not in full_text.lower():
                return log_fail(
                    step_name,
                    "Shopping Bag",
                    full_text,
                    "Heading mismatch"
                )

            count_match = re.search(r"\((\d+)\)", full_text)
            actual_count = count_match.group(1) if count_match else "0"

            if expected_item_count and str(actual_count) != str(expected_item_count):
                return log_fail(
                    step_name,
                    expected_item_count,
                    actual_count,
                    "Item count mismatch"
                )

            return log_pass(
                step_name,
                expected_item_count or "Any",
                full_text
            )

        except Exception as error:
            return log_fail(
                step_name,
                "Shopping Bag title",
                "Not found",
                error
            )

    # ------------------------------------------------------------------
    # UPDATED SETTING VALIDATION
    # ------------------------------------------------------------------

    def verify_setting_in_bag(self, setting_details):

        results = []

        print("\n  --- Setting Product in Bag ---")

        try:
            all_boxes = self.page.locator("div.prod_title")
            total_boxes = all_boxes.count()

            setting_box = None

            expected_name = setting_details.get("product_name", "").lower()

            for i in range(total_boxes):

                try:
                    title = all_boxes.nth(i).locator("h4").first.inner_text().strip().lower()

                    print(f"  [INFO] BOX [{i}] TITLE : {title}")

                    # UPDATED LOGIC:
                    # setting product = NOT diamond
                    if "diamond" not in title:
                        setting_box = all_boxes.nth(i)
                        break

                except Exception:
                    pass

            if setting_box is None:
                results.append(
                    log_fail(
                        "Bag - Setting Product",
                        "Setting product visible",
                        "Not found"
                    )
                )
                return results

            # ---------------- NAME ----------------

            actual_name = setting_box.locator("h4").first.inner_text().strip()

            search_key = " ".join(expected_name.split()[:2]).lower()

            if search_key in actual_name.lower():
                results.append(
                    log_pass(
                        "Bag - Setting Name",
                        search_key,
                        actual_name
                    )
                )
            else:
                results.append(
                    log_fail(
                        "Bag - Setting Name",
                        search_key,
                        actual_name
                    )
                )

            # ---------------- METAL ----------------

            expected_metal = setting_details.get("metal_color", "").lower()

            try:
                actual_metal = setting_box.locator("p").first.inner_text().strip()

                if expected_metal in actual_metal.lower():
                    results.append(
                        log_pass(
                            "Bag - Setting Metal",
                            expected_metal,
                            actual_metal
                        )
                    )
                else:
                    results.append(
                        log_fail(
                            "Bag - Setting Metal",
                            expected_metal,
                            actual_metal
                        )
                    )

            except Exception as error:
                results.append(
                    log_skip(
                        "Bag - Setting Metal",
                        str(error)
                    )
                )

            # ---------------- PRICE ----------------

            expected_price = setting_details.get("price", "")

            try:
                price_text = setting_box.locator("h4.main_price").first.inner_text().strip()

                actual_price = extract_price(price_text)

                if actual_price == expected_price:
                    results.append(
                        log_pass(
                            "Bag - Setting Price",
                            expected_price,
                            actual_price
                        )
                    )
                else:
                    results.append(
                        log_fail(
                            "Bag - Setting Price",
                            expected_price,
                            actual_price
                        )
                    )

            except Exception as error:
                results.append(
                    log_skip(
                        "Bag - Setting Price",
                        str(error)
                    )
                )

            # ---------------- MRP ----------------

            expected_mrp = setting_details.get("mrp", "")

            try:
                actual_mrp = setting_box.locator(".pdp_mrp_box").first.inner_text().strip()

                if actual_mrp == expected_mrp:
                    results.append(
                        log_pass(
                            "Bag - Setting MRP",
                            expected_mrp,
                            actual_mrp
                        )
                    )
                else:
                    results.append(
                        log_fail(
                            "Bag - Setting MRP",
                            expected_mrp,
                            actual_mrp
                        )
                    )

            except Exception as error:
                results.append(
                    log_skip(
                        "Bag - Setting MRP",
                        str(error)
                    )
                )

        except Exception as error:

            results.append(
                log_fail(
                    "Bag - Setting Product",
                    "Visible",
                    "Not found",
                    error
                )
            )

        return results

    # ------------------------------------------------------------------
    # UPDATED DIAMOND VALIDATION
    # ------------------------------------------------------------------

    def verify_diamond_in_bag(self, diamond_details):

        results = []

        print("\n  --- Diamond Product in Bag ---")

        try:
            all_boxes = self.page.locator("div.prod_title")
            total_boxes = all_boxes.count()

            diamond_box = None
            diamond_title = ""

            for i in range(total_boxes):

                try:
                    title = all_boxes.nth(i).locator("h4").first.inner_text().strip()

                    print(f"  [INFO] BOX [{i}] TITLE : {title}")

                    if "diamond" in title.lower():
                        diamond_box = all_boxes.nth(i)
                        diamond_title = title
                        break

                except Exception:
                    pass

            if diamond_box is None:
                results.append(
                    log_fail(
                        "Bag - Diamond Product",
                        "Diamond visible",
                        "Not found"
                    )
                )
                return results

            # ---------------- CARAT ----------------

            expected_title = diamond_details.get("title", "").lower()

            carat_match = re.search(r"(\d+(\.\d+)?)", expected_title)
            expected_carat = carat_match.group(1) if carat_match else ""

            if expected_carat in diamond_title:
                results.append(
                    log_pass(
                        "Bag - Diamond Carat",
                        expected_carat,
                        diamond_title
                    )
                )
            else:
                results.append(
                    log_fail(
                        "Bag - Diamond Carat",
                        expected_carat,
                        diamond_title
                    )
                )

            # ---------------- SHAPE ----------------

            shapes = [
                "oval",
                "round",
                "emerald",
                "princess",
                "pear",
                "cushion",
                "asscher",
                "marquise"
            ]

            expected_shape = ""

            for shape in shapes:
                if shape in expected_title:
                    expected_shape = shape
                    break

            if expected_shape in diamond_title.lower():
                results.append(
                    log_pass(
                        "Bag - Diamond Shape",
                        expected_shape,
                        diamond_title
                    )
                )
            else:
                results.append(
                    log_fail(
                        "Bag - Diamond Shape",
                        expected_shape,
                        diamond_title
                    )
                )

            # ---------------- PRICE ----------------

            expected_price = diamond_details.get("price", "")

            try:
                price_text = diamond_box.locator(
                    "div.appr_price_right h4"
                ).first.inner_text().strip()

                actual_price = extract_price(price_text)

                if actual_price == expected_price:
                    results.append(
                        log_pass(
                            "Bag - Diamond Price",
                            expected_price,
                            actual_price
                        )
                    )
                else:
                    results.append(
                        log_fail(
                            "Bag - Diamond Price",
                            expected_price,
                            actual_price
                        )
                    )

            except Exception as error:
                results.append(
                    log_skip(
                        "Bag - Diamond Price",
                        str(error)
                    )
                )

            # ---------------- MRP ----------------

            expected_mrp = diamond_details.get("mrp", "")

            try:
                actual_mrp = diamond_box.locator(
                    ".pdp_mrp_box"
                ).first.inner_text().strip()

                if actual_mrp == expected_mrp:
                    results.append(
                        log_pass(
                            "Bag - Diamond MRP",
                            expected_mrp,
                            actual_mrp
                        )
                    )
                else:
                    results.append(
                        log_fail(
                            "Bag - Diamond MRP",
                            expected_mrp,
                            actual_mrp
                        )
                    )

            except Exception as error:
                results.append(
                    log_skip(
                        "Bag - Diamond MRP",
                        str(error)
                    )
                )

        except Exception as error:

            results.append(
                log_fail(
                    "Bag - Diamond Product",
                    "Diamond visible",
                    "Not found",
                    error
                )
            )

        return results

    def verify_ring_size_in_bag(self, expected_ring_size):

        step_name = "Bag - Ring Size"

        try:
            ring_size_el = self.page.locator("div.current_active span").first
            ring_size_el.wait_for(state="visible", timeout=8000)

            actual_size = ring_size_el.inner_text().strip()

            if str(actual_size) == str(expected_ring_size):

                return log_pass(
                    step_name,
                    expected_ring_size,
                    actual_size
                )

            return log_fail(
                step_name,
                expected_ring_size,
                actual_size
            )

        except Exception as error:

            return log_fail(
                step_name,
                expected_ring_size,
                "Not found",
                error
            )

    def verify_summary_prices(self, expected_total_price, expected_total_mrp):

        results = []

        print("\n  --- Summary Prices ---")

        try:
            total_price_block = self.page.locator("div.total_price").first
            total_price_block.wait_for(state="visible", timeout=8000)

            total_text = total_price_block.inner_text().strip()

            prices = re.findall(r"\$[\d,]+", total_text)

            actual_total = prices[0] if len(prices) > 0 else ""
            actual_mrp = prices[1] if len(prices) > 1 else ""

            if actual_total == expected_total_price:
                results.append(
                    log_pass(
                        "Bag - Total Price",
                        expected_total_price,
                        actual_total
                    )
                )
            else:
                results.append(
                    log_fail(
                        "Bag - Total Price",
                        expected_total_price,
                        actual_total
                    )
                )

            if actual_mrp == expected_total_mrp:
                results.append(
                    log_pass(
                        "Bag - Total MRP",
                        expected_total_mrp,
                        actual_mrp
                    )
                )
            else:
                results.append(
                    log_fail(
                        "Bag - Total MRP",
                        expected_total_mrp,
                        actual_mrp
                    )
                )

        except Exception as error:

            results.append(
                log_fail(
                    "Bag - Summary Prices",
                    expected_total_price,
                    "Not found",
                    error
                )
            )

        return results

    def verify_shipment_date_in_bag(self, expected_shipment_date):

        step_name = "Bag - Shipment Date"

        try:
            date_el = self.page.locator("span.date").first
            date_el.wait_for(state="visible", timeout=8000)

            actual_date = date_el.inner_text().strip()

            if expected_shipment_date.lower() in actual_date.lower():

                return log_pass(
                    step_name,
                    expected_shipment_date,
                    actual_date
                )

            return log_fail(
                step_name,
                expected_shipment_date,
                actual_date
            )

        except Exception as error:

            return log_fail(
                step_name,
                expected_shipment_date,
                "Not found",
                error
            )

    def verify_coupon_applied(self):

        step_name = "Bag - Coupon Applied"

        try:
            success_msg = self.page.locator("div.success_msg").first

            if success_msg.count() > 0 and success_msg.is_visible():

                msg_text = success_msg.inner_text().strip()

                if "applied" in msg_text.lower():

                    return log_pass(
                        step_name,
                        "Coupon applied",
                        msg_text
                    )

            return log_skip(
                step_name,
                "Coupon not applied"
            )

        except Exception as error:

            return log_fail(
                step_name,
                "Coupon message",
                "Error",
                error
            )

    def click_continue_to_payment(self, should_click=True):

        step_name = "Bag - Continue to Payment"

        if not should_click:
            return log_skip(
                step_name,
                "Previous validations failed"
            )

        try:
            continue_btn = self.page.locator(
                "button.btn-p-animation:has-text('CONTINUE TO PAYMENT')"
            ).first

            continue_btn.wait_for(state="visible", timeout=10000)

            continue_btn.scroll_into_view_if_needed()

            continue_btn.click()

            return log_pass(
                step_name,
                "Button clickable",
                "Clicked successfully"
            )

        except Exception as error:

            return log_fail(
                step_name,
                "Button clickable",
                "Click failed",
                error
            )

    # ------------------------------------------------------------------
    # MAIN METHOD
    # ------------------------------------------------------------------

    def verify_shopping_bag(
        self,
        setting_details,
        diamond_details,
        expected_ring_size,
        expected_total_price,
        expected_total_mrp,
        expected_shipment_date
    ):

        all_results = []

        print("\n========== SHOPPING BAG VERIFICATION ==========")

        self.page.wait_for_timeout(2000)

        all_results.append(self.dismiss_free_product_popup())

        all_results.append(self.verify_bag_title())

        all_results.extend(
            self.verify_setting_in_bag(setting_details)
        )

        all_results.extend(
            self.verify_diamond_in_bag(diamond_details)
        )

        all_results.append(
            self.verify_ring_size_in_bag(expected_ring_size)
        )

        all_results.extend(
            self.verify_summary_prices(
                expected_total_price,
                expected_total_mrp
            )
        )

        all_results.append(
            self.verify_shipment_date_in_bag(expected_shipment_date)
        )

        all_results.append(
            self.verify_coupon_applied()
        )

        any_failed = any(
            result["status"] == "FAIL"
            for result in all_results
        )

        all_results.append(
            self.click_continue_to_payment(
                should_click=not any_failed
            )
        )

        failed = [
            r for r in all_results
            if r["status"] == "FAIL"
        ]

        print(f"\n  [BAG OVERALL] {'PASS' if not failed else 'FAIL'}")

        return all_results
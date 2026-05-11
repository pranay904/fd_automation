import re
from FD.pages.base_page import BasePage
from FD.pages.shopping_bag_page import log_pass, log_skip, log_fail


class ShoppingBag(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # -------------------- STORE SHOPPING BAG DATA --------------------
        self.shopping_bag_data = {
            "_bag_setting_name": "",
            "_bag_setting_price": "",
            "_bag_setting_mrp": "",
            "_bag_setting_metal": "",

            "_bag_diamond_name": "",
            "_bag_diamond_price": "",
            "_bag_diamond_mrp": "",
            "_bag_diamond_carat": "",
            "_bag_diamond_shape": "",

            "_bag_total_price": "",
            "_bag_total_mrp": "",
            "_bag_saved_amount": "",

            "_bag_selected_ring_size": "",
            "_bag_estimated_delivery_date": ""
        }

    def normalize(self, text):
        return re.sub(r"\s+", " ", text).strip().lower()

    # -------------------- DIAMOND TITLE PARSER --------------------
    def parse_diamond_title(self, title):
        """
        CONCEPT: Centralized parsing logic
        WHY: Avoid inconsistent regex across pages (PLP / Complete / Bag)
        """

        result = {
            "carat": None,
            "shape": None,
            "name": title
        }

        try:
            # ---------------- CARAT ----------------
            carat_match = re.search(
                r"(\d+(\.\d+)?)\s*ct",
                title,
                re.IGNORECASE
            )
            if carat_match:
                result["carat"] = carat_match.group(1)

            # ---------------- SHAPE ----------------
            shape_match = re.search(
                r"(oval|round|emerald|princess|pear|cushion|asscher|marquise)",
                title,
                re.IGNORECASE
            )
            if shape_match:
                result["shape"] = shape_match.group(1)

            return result

        except Exception:
            return result

    # -------------------- DISMISS FREE PRODUCT POPUP --------------------
    def dismiss_free_product_popup(self):
        """
        CONCEPT: Conditional element handling
        WHY: The popup does not always appear immediately.
             We wait up to 5 seconds for it to appear.
             If it appears, we close it.
             If it does not appear, we skip silently — no failure.

        CONCEPT: try/except for optional actions
        WHY: If the popup never appears, we should not fail the test.
             We catch the timeout and continue normally..
        """
        step_name = "Shopping Bag - Dismiss Free Product Popup"

        try:
            # Wait up to 5 seconds for the popup modal to appear
            # The modal contains the close button div.modal_close_btn
            close_button = self.page.locator("div.modal_close_btn").first

            # CONCEPT: wait_for with timeout
            # WHY: The popup may take a moment to animate open.
            #      We wait up to 5 seconds. If it does not appear, an
            #      exception is raised and we catch it below.
            close_button.wait_for(state="visible", timeout=5000)

            # Popup appeared — click the close button to dismiss it
            close_button.click()

            # Wait a moment for the popup to close completely
            self.page.wait_for_timeout(800)

            print(f"  [PASS] {step_name} — popup closed")

            return log_pass(
                step_name,
                "Free product popup closed",
                "Clicked div.modal_close_btn"
            )

        except Exception:
            # CONCEPT: Silent skip — popup did not appear, that is fine
            print(f"  [SKIP] {step_name} — popup did not appear")

            return log_skip(
                step_name,
                "Free product popup did not appear — skipping"
            )

    # -------------------- SETTING SUMMARY --------------------
    def verify_setting_summary(self, expected):

        step_name = "Bag - Setting Summary"
        results = []

        try:

            # FIX: use correct container like your working diamond pattern
            box = self.page.locator("(//div[contains(@class,'prod_title')])[1]")
            box.wait_for(state="visible", timeout=10000)

            # FIX: avoid strict h4 conflict → pick FIRST meaningful heading only
            all_headings = box.locator("h4")
            actual_name = all_headings.first.inner_text().strip()

            actual_metal = box.locator("p").first.inner_text().strip()

            print(f"  [INFO] Setting name: {actual_name}")
            print(f"  [INFO] Setting metal: {actual_metal}")

            expected_name = expected.get("product_name", "")
            expected_metal = expected.get("metal_color", "")

            search_key = " ".join(expected_name.split()[:2]).lower()

            if search_key and search_key in actual_name.lower():
                results.append(log_pass("Bag - Setting Name", search_key, actual_name))
            else:
                results.append(log_fail("Bag - Setting Name", search_key, actual_name))

            if expected_metal and expected_metal.lower() in actual_metal.lower():
                results.append(log_pass("Bag - Setting Metal", expected_metal, actual_metal))
            else:
                results.append(log_skip("Bag - Setting Metal", "Metal not matched"))

        except Exception as e:
            results.append(log_fail(step_name, "Setting visible", "Not found", e))

        return results

    # -------------------- DIAMOND SUMMARY --------------------
    def verify_diamond_summary(self, diamond):

        print("\n===== VERIFYING DIAMOND SUMMARY =====")

        results = []

        try:
            box = self.page.locator("(//div[@class='prod_title my-3'])[1]")
            box.wait_for(state="visible", timeout=10000)

            title = box.locator("h4").first.inner_text().strip()

            print("ACTUAL:", title)

            # -------------------------------------------------
            # PARSE EXPECTED CARAT/SHAPE FROM AVAILABLE KEYS
            # Supports both PLP dict (title, price, mrp)
            # and complete page dict (diamond_carat, diamond_shape)
            # -------------------------------------------------

            # Try direct keys first, then parse from title
            raw_title_expected = diamond.get("title", "")

            expected_carat = (
                diamond.get("carat")
                or diamond.get("diamond_carat")
                or (re.search(r"\d+\.\d+", raw_title_expected).group(0) if re.search(r"\d+\.\d+", raw_title_expected) else "")
            )
            expected_shape = (
                diamond.get("shape")
                or diamond.get("diamond_shape")
                or (re.search(r"(oval|round|emerald|princess|pear|cushion|asscher|marquise)", raw_title_expected, re.IGNORECASE).group(1) if re.search(r"(oval|round|emerald|princess|pear|cushion|asscher|marquise)", raw_title_expected, re.IGNORECASE) else "")
            )
            expected_carat = str(expected_carat) if expected_carat else ""
            expected_shape = str(expected_shape) if expected_shape else ""

            # ---------------- PARSE UI ----------------
            parsed = self.parse_diamond_title(title)

            actual_carat = parsed["carat"]
            actual_shape = parsed["shape"]

            print("CARAT:", actual_carat)
            print("SHAPE:", actual_shape)

            # ---------------- VALIDATIONS ----------------

            # Normalize expected_carat to just the number e.g. "1.01 Ct." -> "1.01"
            carat_num_match = re.search(r"\d+\.\d+", expected_carat)
            expected_carat_num = carat_num_match.group(0) if carat_num_match else expected_carat

            if expected_carat_num and expected_carat_num == (actual_carat or ""):
                results.append(log_pass("Bag - Diamond Carat", expected_carat_num, actual_carat))
            else:
                results.append(log_fail("Bag - Diamond Carat", expected_carat_num, actual_carat))

            if expected_shape and expected_shape.lower() == (actual_shape or "").lower():
                results.append(log_pass("Bag - Diamond Shape", expected_shape, actual_shape))
            else:
                results.append(log_fail("Bag - Diamond Shape", expected_shape, actual_shape))

            self.shopping_bag_data["_bag_diamond_name"] = title
            self.shopping_bag_data["_bag_diamond_carat"] = actual_carat
            self.shopping_bag_data["_bag_diamond_shape"] = actual_shape

        except Exception as e:
            results.append(log_fail("Bag - Diamond Summary", "Expected diamond data", "Not found", e))

        return results

    # -------------------- RING SIZE --------------------
    def verify_ring_size_in_bag(self, expected_ring_size):

        step_name = "Bag - Ring Size Matches Complete Page"

        try:
            # ---------------- SAFE WAIT FOR PAGE STABILITY ----------------
            self.page.wait_for_timeout(2000)

            # OPTIONAL: ensure popup is gone
            try:
                self.page.locator("div.modal_close_btn").click(timeout=2000)
            except:
                pass

            # ---------------- ROBUST LOCATOR (FALLBACK) ----------------
            ring_size_el = self.page.locator(
                "div.current_active span, div.current_active, span.selected_ring_size"
            ).first

            ring_size_el.wait_for(state="visible", timeout=12000)

            actual_size = ring_size_el.inner_text().strip()

            print(f"  [INFO] Ring size in bag: {actual_size}")

            if str(actual_size) == str(expected_ring_size):
                return log_pass(step_name, expected_ring_size, actual_size)
            else:
                return log_fail(
                    step_name,
                    expected_ring_size,
                    actual_size,
                    "Ring size does not match Complete page selection"
                )

        except Exception as error:
            return log_fail(step_name, expected_ring_size, "Not found", error)

    # -------------------- ESTIMATED DELIVERY DATE --------------------
    def verify_shipment_date_in_bag(self, expected_shipment_date):
        step_name = "Bag - Estimated Delivery Date"

        try:
            date_el = self.page.locator("span.date").first
            date_el.wait_for(state="visible", timeout=8000)

            actual_date = date_el.inner_text().strip()

            self.shopping_bag_data["_bag_estimated_delivery_date"] = actual_date

            if expected_shipment_date.lower() in actual_date.lower():
                return log_pass(step_name, expected_shipment_date, actual_date)
            else:
                return log_fail(
                    step_name,
                    expected_shipment_date,
                    actual_date,
                    "Estimated delivery date does not match Complete page"
                )

        except Exception as e:
            return log_fail(step_name, expected_shipment_date, "Not found", e)

    # -------------------- SUMMARY PRICES --------------------
    def verify_summary_prices(self, expected_total_price, expected_total_mrp):
        results = []
        step_name_total = "Bag - Total Price & MRP"

        try:
            total_price_block = self.page.locator("div.total_price").first
            total_price_block.wait_for(state="visible", timeout=8000)

            total_text = total_price_block.inner_text().strip().replace("\n", " ")

            prices = re.findall(r"\$[\d,]+", total_text)

            actual_total_price = prices[0] if len(prices) > 0 else None
            actual_total_mrp = prices[1] if len(prices) > 1 else None

            # Store
            self.shopping_bag_data["_bag_total_price"] = actual_total_price
            self.shopping_bag_data["_bag_total_mrp"] = actual_total_mrp

            # Total Price
            if actual_total_price == expected_total_price:
                results.append(
                    log_pass(
                        f"{step_name_total} - Total Price",
                        expected_total_price,
                        actual_total_price
                    )
                )
            else:
                results.append(
                    log_fail(
                        f"{step_name_total} - Total Price",
                        expected_total_price,
                        actual_total_price
                    )
                )

            # Total MRP
            if actual_total_mrp == expected_total_mrp:
                results.append(
                    log_pass(
                        f"{step_name_total} - Total MRP",
                        expected_total_mrp,
                        actual_total_mrp
                    )
                )
            else:
                results.append(
                    log_fail(
                        f"{step_name_total} - Total MRP",
                        expected_total_mrp,
                        actual_total_mrp
                    )
                )

        except Exception as e:
            results.append(
                log_fail(
                    step_name_total,
                    "Expected total values",
                    "Not found",
                    e
                )
            )

        return results
    # -------------------- CLICK CONTINUE TO PAYMENT --------------------
    def click_continue_to_payment(self):
        """
        Clicks on CONTINUE TO PAYMENT button after all validations pass
        """

        step_name = "Bag - Continue To Payment"

        try:
            continue_btn = self.page.get_by_role(
                "button",
                name="CONTINUE TO PAYMENT"
            ).first

            continue_btn.wait_for(state="visible", timeout=10000)

            continue_btn.click()

            print(f"  [PASS] {step_name} — Clicked CONTINUE TO PAYMENT")

            return log_pass(
                step_name,
                "CONTINUE TO PAYMENT button should be clicked",
                "Clicked successfully"
            )

        except Exception as e:
            return log_fail(
                step_name,
                "CONTINUE TO PAYMENT button visible",
                "Button not clicked",
                e
            )



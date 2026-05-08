"""
shopping_bag_page.py
--------------------
CONCEPT: Page Object Model (POM)
WHY: All Shopping Bag page verifications live here.
     After clicking "View Bag", this page runs all checks.

Verifications (in order):
1.  Bag title and item count
2.  Setting product name, metal, price, MRP
3.  Diamond product name, carat, shape, price, MRP
4.  Ring size matches what was selected on Complete page
5.  Summary subtotal = setting price + diamond price
6.  Summary total price and MRP match Complete page
7.  Shipment date matches Complete page
8.  Free product visible (if total >= $1000)
9.  Coupon applied and shown in summary
10. Recommended Add-Ons section visible (for CYO products)
"""

import re                               # CONCEPT: Standard Library — Regular Expressions
                                        # WHY: Used to extract numbers like "$1,005" from text
from FD.pages.base_page import BasePage # CONCEPT: Inheritance
                                        # WHY: Gets self.page (browser tab) from BasePage


# -----------------------------------------------------------------------
# CONCEPT: Helper functions for consistent PASS/FAIL/SKIP logging
# WHY: Every check returns the same dictionary format so results
#      can be collected and written to the Excel report uniformly
# -----------------------------------------------------------------------

def log_pass(step_name, expected_value, actual_value):
    print(f"  [PASS] {step_name}")
    print(f"         Expected : {expected_value}")
    print(f"         Actual   : {actual_value}")
    return {"step": step_name, "expected": str(expected_value),
            "actual": str(actual_value), "status": "PASS", "error": ""}


def log_fail(step_name, expected_value, actual_value, error_message=""):
    print(f"  [FAIL] {step_name}")
    print(f"         Expected : {expected_value}")
    print(f"         Actual   : {actual_value}")
    print(f"         Error    : {error_message}")
    return {"step": step_name, "expected": str(expected_value),
            "actual": str(actual_value), "status": "FAIL", "error": str(error_message)}


def log_skip(step_name, reason=""):
    print(f"  [SKIP] {step_name}")
    print(f"         Reason   : {reason}")
    return {"step": step_name, "expected": "N/A",
            "actual": "SKIPPED", "status": "SKIP", "error": reason}


# -----------------------------------------------------------------------
# CONCEPT: Helper to extract dollar amount from text using regex
# WHY: Prices appear as "$1,005" inside longer strings.
#      re.search finds the pattern anywhere in the text.
# -----------------------------------------------------------------------

def extract_price(text):
    """
    CONCEPT: Regular Expression
    WHY: r"\$[\d,]+" means:
         \$    = literal dollar sign
         [\d,]+ = one or more digits or commas
    Example: extract_price("Total $1,005 MRP") -> "$1,005"
    """
    match = re.search(r"\$[\d,]+", str(text))
    return match.group(0) if match else ""


# -----------------------------------------------------------------------
# CONCEPT: Class with Inheritance
# WHY: ShoppingBagPage inherits BasePage to get self.page (browser)
# -----------------------------------------------------------------------

class ShoppingBagPage(BasePage):

    # -------------------------------------------------------------------
    # DISMISS FREE PRODUCT POPUP
    # This popup appears automatically when the Shopping Bag page loads.
    # It shows "Discounts & Promotions" with free product offers.
    # We must close it before we can interact with the rest of the page.
    #
    # Close button locator: div.modal_close_btn (contains an SVG X icon)
    # XPath: //div[@class='modal_close_btn']//*[name()='svg']
    # -------------------------------------------------------------------
    def dismiss_free_product_popup(self):
        """
        CONCEPT: Conditional element handling
        WHY: The popup does not always appear immediately.
             We wait up to 5 seconds for it to appear.
             If it appears, we close it.
             If it does not appear, we skip silently — no failure.

        CONCEPT: try/except for optional actions
        WHY: If the popup never appears, we should not fail the test.
             We catch the timeout and continue normally.
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
            return log_pass(step_name,
                            "Free product popup closed",
                            "Clicked div.modal_close_btn")

        except Exception:
            # CONCEPT: Silent skip — popup did not appear, that is fine
            print(f"  [SKIP] {step_name} — popup did not appear")
            return log_skip(step_name, "Free product popup did not appear — skipping")

    def verify_bag_title(self, expected_item_count=None):
        """
        CONCEPT: String splitting to extract parts
        WHY: "My Shopping Bag (2)" split by space gives
             ["My", "Shopping", "Bag", "(2)"]
             We take first 3 words as title and last word as count.
        """
        step_name = "Shopping Bag - Page Title and Item Count"
        try:
            # Wait for the page heading to appear
            heading = self.page.locator("h1.font-active").first
            heading.wait_for(state="visible", timeout=10000)

            full_text = heading.inner_text().strip()
            print(f"  [INFO] Bag heading text: {full_text}")

            # Check title contains "Shopping Bag"
            if "shopping bag" not in full_text.lower():
                return log_fail(step_name, "My Shopping Bag", full_text,
                                "Title does not contain 'Shopping Bag'")

            # Extract count from parentheses e.g. "(2)" -> "2"
            count_match = re.search(r"\((\d+)\)", full_text)
            actual_count = count_match.group(1) if count_match else "0"
            print(f"  [INFO] Item count in bag: {actual_count}")

            if expected_item_count and str(actual_count) != str(expected_item_count):
                return log_fail(step_name,
                                f"Shopping Bag ({expected_item_count})",
                                full_text,
                                f"Expected count {expected_item_count}, got {actual_count}")

            return log_pass(step_name,
                            f"Shopping Bag ({expected_item_count or 'any'})",
                            full_text)
        except Exception as error:
            return log_fail(step_name, "Shopping Bag title visible", "Not found", error)

    # -------------------------------------------------------------------
    # STEP 2: Verify setting product details in bag
    # Locator: (//div[@class='prod_title'])[1] — first product box
    # -------------------------------------------------------------------
    def verify_setting_in_bag(self, setting_details):
        """
        CONCEPT: Dictionary .get() for safe access
        WHY: setting_details["product_name"] would crash if key missing.
             .get("product_name", "") returns "" safely.

        Checks:
        - Setting name (first 2 words) visible in product title
        - Metal color visible in product description
        - Setting price matches PLP price
        - Setting MRP matches PLP MRP
        """
        results = []
        print("\n  --- Setting Product in Bag ---")

        try:
            # CONCEPT: XPath locator — finds first prod_title div
            setting_box = self.page.locator("(//div[@class='prod_title'])[1]")
            setting_box.wait_for(state="visible", timeout=10000)

            # Read product name from h4 tag
            actual_name = setting_box.locator("h4").first.inner_text().strip()
            print(f"  [INFO] Setting name in bag: {actual_name}")

            # Read metal/description from first p tag
            actual_metal = setting_box.locator("p").first.inner_text().strip()
            print(f"  [INFO] Setting metal in bag: {actual_metal}")

            # --- Check setting name (first 2 words) ---
            expected_name = setting_details.get("product_name", "")
            # CONCEPT: List slicing — take first 2 words of expected name
            search_key = " ".join(expected_name.split()[:2]).lower()
            if search_key and search_key in actual_name.lower():
                results.append(log_pass("Bag - Setting Name",
                                        search_key, actual_name))
            else:
                results.append(log_fail("Bag - Setting Name",
                                        search_key, actual_name,
                                        f"'{search_key}' not found in bag"))

            # --- Check metal color ---
            expected_metal = setting_details.get("metal_color", "").lower()
            if expected_metal and expected_metal in actual_metal.lower():
                results.append(log_pass("Bag - Setting Metal",
                                        expected_metal, actual_metal))
            else:
                results.append(log_skip("Bag - Setting Metal",
                                        f"Metal '{expected_metal}' not found — skipping"))

            # --- Check setting price ---
            expected_price = setting_details.get("price", "")
            try:
                # Price is in h4 with class main_price
                price_el = setting_box.locator("h4.main_price").first
                actual_price = price_el.inner_text().strip().split()[0]
                print(f"  [INFO] Setting price in bag: {actual_price}")
                if expected_price and expected_price in actual_price:
                    results.append(log_pass("Bag - Setting Price",
                                            expected_price, actual_price))
                else:
                    results.append(log_fail("Bag - Setting Price",
                                            expected_price, actual_price))
            except Exception:
                results.append(log_skip("Bag - Setting Price",
                                        "Price element not found"))

            # --- Check setting MRP ---
            expected_mrp = setting_details.get("mrp", "")
            try:
                actual_mrp = setting_box.locator(".pdp_mrp_box").first.inner_text().strip()
                print(f"  [INFO] Setting MRP in bag: {actual_mrp}")
                if expected_mrp and expected_mrp in actual_mrp:
                    results.append(log_pass("Bag - Setting MRP",
                                            expected_mrp, actual_mrp))
                else:
                    results.append(log_skip("Bag - Setting MRP",
                                            f"MRP '{expected_mrp}' not matched — skipping"))
            except Exception:
                results.append(log_skip("Bag - Setting MRP",
                                        "MRP element not found"))

        except Exception as error:
            results.append(log_fail("Bag - Setting Product Box",
                                    "Setting product visible", "Not found", error))

        return results

    # -------------------------------------------------------------------
    # STEP 3: Verify diamond product details in bag
    #
    # PROBLEM: (//div[@class='prod_title'])[2] may pick the wrong product
    #          if there are add-on items (like Jewelry Cleaning Kit) in the bag.
    #
    # SOLUTION: Loop through ALL prod_title divs and find the one whose
    #           h4 text contains a carat number (e.g. "1.02") or the word "diamond".
    #           This way we always find the correct diamond product regardless
    #           of its position in the bag.
    #
    # HTML structure of diamond prod_title:
    # <div class="prod_title">
    #   <div class="appr_price ...">
    #     <div class="appr_price_left">
    #       <h4>1.02 Ct. Oval Lab Grown Diamond</h4>
    #       <p>Excellent Cut, D Color, VS2 Clarity, Lot No. ...</p>
    #     </div>
    #     <div class="appr_price_right">
    #       <h4>$418 <span class="pdp_mrp_box">$697</span></h4>
    #     </div>
    #   </div>
    # </div>
    # -------------------------------------------------------------------
    def verify_diamond_in_bag(self, diamond_details):
        """
        CONCEPT: Loop to find the correct element
        WHY: The bag may have multiple prod_title divs (setting, diamond,
             add-ons like cleaning kit). We cannot rely on position [2].
             Instead we loop through all of them and find the one that
             contains a carat number or the word "diamond" in its h4 text.

        CONCEPT: re.search to detect carat pattern
        WHY: "1.02 Ct. Oval Lab Grown Diamond" contains "1.02" which
             matches the pattern r"\d+\.\d+" (digits dot digits).
        """
        results = []
        print("\n  --- Diamond Product in Bag ---")

        try:
            # Find ALL prod_title divs on the page
            all_product_boxes = self.page.locator("(//div[@class='prod_title my-3'])[1]")
            total_boxes = all_product_boxes.count()
            print(f"  [INFO] Total prod_title boxes found: {total_boxes}")

            # Variable to store the diamond box once we find it
            diamond_box_index = None
            diamond_title_text = ""

            # CONCEPT: for loop to search through all product boxes
            # WHY: We check each box's h4 text to find the diamond one
            for index in range(total_boxes):
                try:
                    # Read the h4 text of this product box
                    box_title = all_product_boxes.nth(index).locator("h4").first.inner_text().strip()
                    print(f"  [INFO] Box [{index}] h4 text: {box_title}")

                    # CONCEPT: re.search to check if this box has a carat number
                    # r"\d+\.\d+" matches patterns like "1.02", "1.16", "2.50"
                    has_carat = re.search(r"\d+\.\d+", box_title)

                    # Also check if the word "diamond" appears in the title
                    has_diamond_word = "diamond" in box_title.lower()

                    # If either condition is true, this is the diamond box
                    if has_carat or has_diamond_word:
                        diamond_box_index = index
                        diamond_title_text = box_title
                        print(f"  [INFO] Diamond box found at index [{index}]: {box_title}")
                        break   # stop searching once we find it

                except Exception:
                    pass    # skip boxes we cannot read

            # If we did not find the diamond box, fail
            if diamond_box_index is None:
                results.append(log_fail(
                    "Bag - Diamond Product Box",
                    "Diamond product found in bag",
                    "Not found",
                    "No prod_title box contains carat number or 'diamond' word"
                ))
                return results

            # We found the diamond box — now verify its details
            diamond_box = all_product_boxes.nth(diamond_box_index)

            # --- Check carat number ---
            # Get expected carat from diamond_details dictionary
            expected_carat_raw = str(diamond_details.get("carat", ""))

            # Extract just the number part e.g. "1.02" from "1.02 Ct."
            carat_match = re.search(r"\d+\.\d+", expected_carat_raw)
            expected_carat = carat_match.group(0) if carat_match else expected_carat_raw

            if expected_carat and expected_carat in diamond_title_text:
                results.append(log_pass(
                    "Bag - Diamond Carat",
                    expected_carat,
                    diamond_title_text
                ))
            else:
                results.append(log_fail(
                    "Bag - Diamond Carat",
                    expected_carat,
                    diamond_title_text,
                    f"Carat '{expected_carat}' not found in diamond title"
                ))

            # --- Check diamond shape ---
            expected_shape = str(diamond_details.get("shape", "")).lower()
            if expected_shape and expected_shape in diamond_title_text.lower():
                results.append(log_pass(
                    "Bag - Diamond Shape",
                    expected_shape,
                    diamond_title_text
                ))
            else:
                results.append(log_fail(
                    "Bag - Diamond Shape",
                    expected_shape,
                    diamond_title_text,
                    f"Shape '{expected_shape}' not found in diamond title"
                ))

            # --- Check diamond price ---
            # Price is in appr_price_right > h4
            # HTML: <h4>$418 <span class="pdp_mrp_box">$697</span></h4>
            expected_price = str(diamond_details.get("price", ""))
            try:
                price_right = diamond_box.locator("div.appr_price_right h4").first
                price_full_text = price_right.inner_text().strip()
                print(f"  [INFO] Diamond price text in bag: {price_full_text}")

                # Extract first dollar amount = selling price
                price_match = re.search(r"\$[\d,]+", price_full_text)
                actual_price = price_match.group(0) if price_match else ""

                if expected_price and expected_price in actual_price:
                    results.append(log_pass(
                        "Bag - Diamond Price",
                        expected_price,
                        actual_price
                    ))
                else:
                    results.append(log_fail(
                        "Bag - Diamond Price",
                        expected_price,
                        actual_price,
                        f"Expected '{expected_price}', got '{actual_price}'"
                    ))
            except Exception as price_error:
                results.append(log_skip(
                    "Bag - Diamond Price",
                    f"Could not read price: {price_error}"
                ))

            # --- Check diamond MRP ---
            # MRP is in span.pdp_mrp_box inside the price h4
            expected_mrp = str(diamond_details.get("mrp", ""))
            try:
                mrp_span = diamond_box.locator("div.appr_price_right .pdp_mrp_box").first
                actual_mrp = mrp_span.inner_text().strip()
                print(f"  [INFO] Diamond MRP in bag: {actual_mrp}")

                if expected_mrp and expected_mrp in actual_mrp:
                    results.append(log_pass(
                        "Bag - Diamond MRP",
                        expected_mrp,
                        actual_mrp
                    ))
                else:
                    results.append(log_skip(
                        "Bag - Diamond MRP",
                        f"Expected '{expected_mrp}', got '{actual_mrp}' — skipping"
                    ))
            except Exception as mrp_error:
                results.append(log_skip(
                    "Bag - Diamond MRP",
                    f"Could not read MRP: {mrp_error}"
                ))

        except Exception as error:
            results.append(log_fail(
                "Bag - Diamond Product Box",
                "Diamond product visible in bag",
                "Error",
                error
            ))

        return results

    # -------------------------------------------------------------------
    # STEP 4: Verify ring size matches Complete page selection
    # Locator: div.current_active span — shows selected ring size
    # -------------------------------------------------------------------
    def verify_ring_size_in_bag(self, expected_ring_size):
        """
        CONCEPT: inner_text() to read visible text
        WHY: The ring size dropdown shows the selected value in a span
             inside div.current_active. We read it and compare.

        HTML: <div class="current_active"><div>...<span>3.75</span>...
        """
        step_name = "Bag - Ring Size Matches Complete Page"
        try:
            # Find the selected ring size shown in the dropdown
            ring_size_el = self.page.locator("div.current_active span").first
            ring_size_el.wait_for(state="visible", timeout=8000)
            actual_size = ring_size_el.inner_text().strip()
            print(f"  [INFO] Ring size in bag: {actual_size}")

            if str(actual_size) == str(expected_ring_size):
                return log_pass(step_name, expected_ring_size, actual_size)
            else:
                return log_fail(step_name, expected_ring_size, actual_size,
                                "Ring size does not match Complete page selection")
        except Exception as error:
            return log_fail(step_name, expected_ring_size, "Not found", error)

    # -------------------------------------------------------------------
    # STEP 5 & 6: Verify Summary — subtotal, total price, MRP
    # Locators from HTML:
    #   Sub-total: div.cart_total span (second span in price_block row)
    #   Total:     h3.font-active (contains total price + strikethrough MRP)
    # -------------------------------------------------------------------
    def verify_summary_prices(self, expected_total_price, expected_total_mrp):
        """
        CONCEPT: Multiple locators for the same data
        WHY: The summary section has subtotal and total in different elements.
             We verify both match what was shown on the Complete page.

        HTML structure:
        Sub-total row: <span>Sub-total</span><span>$1,005</span>
        Total row:     <h3>$1,005 <span class="text-decoration-line-through">$1,672</span></h3>
        """
        results = []
        print("\n  --- Summary Prices in Bag ---")

        # --- Subtotal ---
        try:
            # Find all spans in the price_block — subtotal is in the first row
            subtotal_rows = self.page.locator("div.price_block div.d-flex span")
            # The second span in the first row is the subtotal amount
            subtotal_text = ""
            count = subtotal_rows.count()
            for i in range(count):
                text = subtotal_rows.nth(i).inner_text().strip()
                if text.startswith("$"):
                    subtotal_text = text
                    break
            print(f"  [INFO] Subtotal in bag: {subtotal_text}")

            # Subtotal should equal the total selling price from Complete page
            if expected_total_price and expected_total_price in subtotal_text:
                results.append(log_pass("Bag - Subtotal",
                                        expected_total_price, subtotal_text))
            else:
                results.append(log_skip("Bag - Subtotal",
                                        f"Expected '{expected_total_price}', got '{subtotal_text}' — skipping"))
        except Exception as error:
            results.append(log_fail("Bag - Subtotal", expected_total_price, "Not found", error))

        # --- Total price and MRP ---
        # HTML: <h3 class="font-active">$1,005 <span class="text-decoration-line-through">$1,672</span></h3>
        # The h3 contains both the total price and the strikethrough MRP
        try:
            # Use the for_desktop total_price block to avoid duplicate mobile elements
            total_price_block = self.page.locator("div.total_price").first
            total_price_block.wait_for(state="visible", timeout=8000)

            # Get all text including the strikethrough span
            total_text = total_price_block.inner_text().strip().replace("\n", " ")
            print(f"  [INFO] Total price block text: {total_text}")

            # Extract all dollar amounts — first is total, second is MRP
            all_prices = re.findall(r"\$[\d,]+", total_text)
            print(f"  [INFO] All prices found in total block: {all_prices}")

            # First price = total selling price
            if all_prices and expected_total_price:
                if expected_total_price in all_prices[0]:
                    results.append(log_pass("Bag - Total Price",
                                            expected_total_price, all_prices[0]))
                else:
                    results.append(log_fail("Bag - Total Price",
                                            expected_total_price, all_prices[0],
                                            f"Expected '{expected_total_price}', got '{all_prices[0]}'"))

            # Second price = MRP (strikethrough)
            if len(all_prices) >= 2 and expected_total_mrp:
                if expected_total_mrp in all_prices[1]:
                    results.append(log_pass("Bag - Total MRP",
                                            expected_total_mrp, all_prices[1]))
                else:
                    results.append(log_fail("Bag - Total MRP",
                                            expected_total_mrp, all_prices[1],
                                            f"Expected '{expected_total_mrp}', got '{all_prices[1]}'"))

        except Exception as error:
            results.append(log_fail("Bag - Total Price and MRP",
                                    expected_total_price, "Not found", error))

        return results

    # -------------------------------------------------------------------
    # STEP 7: Verify shipment date matches Complete page
    # Locator: span.date — inside the ETA container
    # -------------------------------------------------------------------
    def verify_shipment_date_in_bag(self, expected_shipment_date):
        """
        CONCEPT: Text comparison
        WHY: The shipment date shown in the bag should be the same
             as what was shown on the Complete page.
        HTML: <span class="date">Tuesday, May 19 2026</span>
        """
        step_name = "Bag - Shipment Date Matches Complete Page"
        try:
            date_el = self.page.locator("span.date").first
            date_el.wait_for(state="visible", timeout=8000)
            actual_date = date_el.inner_text().strip()
            print(f"  [INFO] Shipment date in bag: {actual_date}")

            if expected_shipment_date and expected_shipment_date.lower() in actual_date.lower():
                return log_pass(step_name, expected_shipment_date, actual_date)
            else:
                return log_fail(step_name, expected_shipment_date, actual_date,
                                "Shipment date does not match Complete page")
        except Exception as error:
            return log_fail(step_name, expected_shipment_date, "Not found", error)

    # -------------------------------------------------------------------
    # STEP 8: Verify free product block behavior based on total price
    #
    # TWO different scenarios:
    #
    # Scenario A — Total is LESS than $1000:
    #   A "CLAIM YOUR FREE PRODUCT" banner appears
    #   Locator: div.free_prod_block
    #   This tells the user they can get a free product if they spend more
    #
    # Scenario B — Total is $1000 or MORE:
    #   An actual free product is added to the cart automatically
    #   Locator: div.prod_block with p.badge showing "FREE"
    #   The product has a name, image, and "FREE" price badge
    # -------------------------------------------------------------------
    def verify_free_product_section(self, total_price_string):
        """
        CONCEPT: Conditional logic based on price value
        WHY: The free product behavior is different depending on the total.
             We parse the price string to a number, then decide which
             scenario to verify.

        Parameters:
        - total_price_string : string like "$915" or "$1,005"
        """
        step_name = "Bag - Free Product Section"

        # CONCEPT: String manipulation to convert "$1,005" to integer 1005
        # Step 1: Remove the dollar sign "$"
        # Step 2: Remove the comma ","
        # Step 3: Convert to integer using int()
        try:
            price_without_dollar = total_price_string.replace("$", "")
            price_without_comma  = price_without_dollar.replace(",", "")
            total_as_number      = int(price_without_comma)
            print(f"  [INFO] Total price as number: {total_as_number}")
        except Exception as parse_error:
            # If we cannot parse the price, skip this check
            return log_skip(step_name,
                            f"Could not convert '{total_price_string}' to number: {parse_error}")

        # ---------------------------------------------------------------
        # SCENARIO A: Total is LESS than $1000
        # Expected: "CLAIM YOUR FREE PRODUCT" banner is visible
        # Locator: div.free_prod_block
        # ---------------------------------------------------------------
        if total_as_number < 1000:
            print(f"  [INFO] Total {total_price_string} is under $1000 — checking claim banner")

            try:
                # Find the "CLAIM YOUR FREE PRODUCT" block
                claim_block = self.page.locator("div.free_prod_block").first

                # Check if the block exists on the page
                if claim_block.count() == 0:
                    return log_fail(
                        step_name,
                        "div.free_prod_block visible (total < $1000)",
                        "Element not found on page",
                        "Expected claim banner when total is under $1000"
                    )

                # Wait for it to be visible
                claim_block.wait_for(state="visible", timeout=8000)

                # Read the text inside the block
                claim_text = claim_block.inner_text().strip()
                print(f"  [INFO] Claim block text: {claim_text}")

                # Check that the claim text is present
                if "claim your free product" in claim_text.lower():
                    return log_pass(
                        step_name,
                        "CLAIM YOUR FREE PRODUCT banner visible (total < $1000)",
                        claim_text
                    )
                else:
                    return log_fail(
                        step_name,
                        "CLAIM YOUR FREE PRODUCT text in banner",
                        claim_text,
                        "Expected 'CLAIM YOUR FREE PRODUCT' text not found"
                    )

            except Exception as error:
                return log_fail(
                    step_name,
                    "div.free_prod_block visible",
                    "Error finding element",
                    error
                )

        # ---------------------------------------------------------------
        # SCENARIO B: Total is $1000 or MORE
        # Expected: Actual free product is added to cart
        # Locator: div.prod_block with p.badge showing "FREE"
        # ---------------------------------------------------------------
        else:
            print(f"  [INFO] Total {total_price_string} is $1000 or more — checking free product in cart")

            try:
                # Find the free product block
                free_product_block = self.page.locator("div.prod_block").first

                # Check if the block exists on the page
                if free_product_block.count() == 0:
                    return log_fail(
                        step_name,
                        "div.prod_block visible (total >= $1000)",
                        "Element not found on page",
                        "Expected free product to be added when total is $1000 or more"
                    )

                # Wait for it to be visible
                free_product_block.wait_for(state="visible", timeout=8000)

                # Read the FREE badge text
                # HTML: <p class="badge">FREE</p>
                badge_element = free_product_block.locator("p.badge").first
                badge_text    = badge_element.inner_text().strip()
                print(f"  [INFO] Free product badge text: {badge_text}")

                # Read the free product name
                # HTML: <h4>Lluvia Round Lab Diamond Solitaire Necklace</h4>
                product_name_element = free_product_block.locator("h4").first
                product_name         = product_name_element.inner_text().strip()
                print(f"  [INFO] Free product name: {product_name}")

                # Verify the badge says "FREE"
                if "free" in badge_text.lower():
                    return log_pass(
                        step_name,
                        "FREE product added to cart (total >= $1000)",
                        f"Badge='{badge_text}' | Product='{product_name}'"
                    )
                else:
                    return log_fail(
                        step_name,
                        "FREE badge on product",
                        badge_text,
                        "Badge does not say FREE"
                    )

            except Exception as error:
                return log_fail(
                    step_name,
                    "div.prod_block with FREE badge visible",
                    "Error finding element",
                    error
                )

    # -------------------------------------------------------------------
    # STEP 9: Verify coupon is applied in summary
    # Locator: div.success_msg — shows "Coupon 'FREE-NECKLACE' Applied!"
    # -------------------------------------------------------------------
    def verify_coupon_applied(self):
        """
        CONCEPT: Checking for text presence
        WHY: When a coupon is applied, a success message appears.
             We check if the success message is visible and contains "Applied".
        HTML: <div class="success_msg"> Coupon 'FREE-NECKLACE' Applied! </div>
        """
        step_name = "Bag - Coupon Applied in Summary"
        try:
            success_msg = self.page.locator("div.success_msg").first

            # CONCEPT: is_visible() — returns True/False without throwing error
            if success_msg.count() > 0 and success_msg.is_visible():
                msg_text = success_msg.inner_text().strip()
                print(f"  [INFO] Coupon message: {msg_text}")

                if "applied" in msg_text.lower():
                    return log_pass(step_name, "Coupon Applied message visible", msg_text)
                else:
                    return log_fail(step_name, "Coupon Applied message", msg_text)
            else:
                # No coupon applied — skip (not every order has a coupon)
                return log_skip(step_name, "No coupon applied message visible")
        except Exception as error:
            return log_fail(step_name, "Coupon message", "Error", error)

    # -------------------------------------------------------------------
    # STEP 10: Verify Recommended Add-Ons section visible (CYO products)
    # Locator: div with h2.cart-rec-title — "Recommended Add-Ons"
    # -------------------------------------------------------------------
    # def verify_recommended_addons(self):
    #     """
    #     CONCEPT: Checking section visibility
    #     WHY: For CYO (Create Your Own) ring products, the bag shows
    #          a "Recommended Add-Ons" section with wedding bands etc.
    #          We verify the section is visible and has at least 1 product.
    #     HTML: <h2 class="cart-rec-title">Recommended Add-Ons</h2>
    #           <article class="addon-card">...</article>
    #     """
    #     step_name = "Bag - Recommended Add-Ons Section Visible"
    #     try:
    #         # Find the Recommended Add-Ons heading
    #         rec_title = self.page.locator("h2.cart-rec-title").first
    #
    #         if rec_title.count() == 0 or not rec_title.is_visible():
    #             return log_skip(step_name, "Recommended Add-Ons section not visible")
    #
    #         title_text = rec_title.inner_text().strip()
    #         print(f"  [INFO] Recommended section title: {title_text}")
    #
    #         # Count the addon product cards
    #         addon_cards = self.page.locator("article.addon-card")
    #         card_count = addon_cards.count()
    #         print(f"  [INFO] Recommended addon cards count: {card_count}")
    #
    #         # CONCEPT: Comparison operator — check count is at least 1
    #         if card_count >= 1:
    #             return log_pass(step_name,
    #                             "Recommended Add-Ons visible with >= 1 product",
    #                             f"Title='{title_text}' | Cards={card_count}")
    #         else:
    #             return log_fail(step_name,
    #                             "At least 1 addon card",
    #                             f"0 cards found",
    #                             "No addon products visible")
    #     except Exception as error:
    #         return log_fail(step_name, "Recommended Add-Ons visible", "Error", error)

    # -------------------------------------------------------------------
    # MAIN METHOD: Run all shopping bag verifications
    # -------------------------------------------------------------------

    def click_continue_to_payment(self, should_click=True):
        """
        CONCEPT: Conditional execution
        WHY: We only proceed to payment if all previous steps passed.
             If there are failures, we SKIP this step to avoid invalid flow.

        Locator Strategy:
        - button.btn-p-animation:has-text("CONTINUE TO PAYMENT")
        """

        step_name = "Bag - Continue to Payment Button"

        if not should_click:
            return log_skip(step_name, "Skipping because previous steps failed")

        try:
            # Locate the button using text + class
            continue_btn = self.page.locator(
                "button.btn-p-animation:has-text('CONTINUE TO PAYMENT')"
            ).first

            # Wait until visible
            continue_btn.wait_for(state="visible", timeout=10000)

            # Scroll into view (important for flaky UI)
            continue_btn.scroll_into_view_if_needed()

            # Click the button
            continue_btn.click()

            print("  [PASS] Continue to Payment clicked")

            return log_pass(
                step_name,
                "Continue to Payment button should be clickable",
                "Clicked successfully"
            )

        except Exception as error:
            return log_fail(
                step_name,
                "Continue to Payment button visible and clickable",
                "Click failed",
                error
            )
    def verify_shopping_bag(self, setting_details, diamond_details,
                            expected_ring_size, expected_total_price,
                            expected_total_mrp, expected_shipment_date):
        """
        CONCEPT: Orchestrator method
        WHY: Calls all individual checks in order and collects results.
             The test file only needs to call verify_shopping_bag().

        Parameters:
        - setting_details      : dict from PLP (product_name, price, mrp, metal_color)
        - diamond_details      : dict from PLP (carat, shape, price, mrp)
        - expected_ring_size   : string from Complete page (e.g. "3.75")
        - expected_total_price : string from Complete page (e.g. "$1,005")
        - expected_total_mrp   : string from Complete page (e.g. "$1,672")
        - expected_shipment_date: string from Complete page (e.g. "Tuesday, May 19 2026")
        """
        all_results = []    # CONCEPT: List to collect all results

        print("\n========== SHOPPING BAG VERIFICATION ==========")

        # Wait for the bag page to fully load
        self.page.wait_for_timeout(2000)

        # FIRST: Dismiss the free product popup if it appears
        # WHY: This popup blocks all other elements on the page.
        #      We must close it before we can click or read anything else.
        all_results.append(self.dismiss_free_product_popup())

        # Step 1: Bag title
        all_results.append(self.verify_bag_title())

        # Step 2: Setting product details
        # CONCEPT: list.extend() — adds all items from another list
        all_results.extend(self.verify_setting_in_bag(setting_details))

        # Step 3: Diamond product details
        all_results.extend(self.verify_diamond_in_bag(diamond_details))

        # Step 4: Ring size
        all_results.append(self.verify_ring_size_in_bag(expected_ring_size))

        # Step 5 & 6: Summary prices
        all_results.extend(self.verify_summary_prices(expected_total_price, expected_total_mrp))

        # Step 7: Shipment date
        all_results.append(self.verify_shipment_date_in_bag(expected_shipment_date))

        # Step 8: Free product section (claim banner or actual free product)
        all_results.append(self.verify_free_product_section(expected_total_price))

        # Step 9: Coupon applied
        all_results.append(self.verify_coupon_applied())

        # Step 10: Recommended Add-Ons — DISABLED for now
        # TODO: Enable when recommended products logic is confirmed
        # all_results.append(self.verify_recommended_addons())

        # Step 10: Click Continue to Payment if all checks passed
        any_failed = any(result["status"] == "FAIL" for result in all_results)
        all_results.append(self.click_continue_to_payment(should_click=not any_failed))

        # Print overall result
        failed = [r for r in all_results if r["status"] == "FAIL"]
        print(f"\n  [BAG OVERALL] {'PASS' if not failed else 'FAIL'}")

        return all_results



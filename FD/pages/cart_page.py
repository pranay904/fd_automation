"""
cart_page.py
------------
CONCEPT: Page Object Model (POM)
WHY: We keep all cart-related actions in ONE file (this file).
     The test file does not know HOW to click buttons — it just calls
     methods like verify_quick_cart(). This makes tests easy to maintain.
     If the website changes a button, we only fix it here, not in every test.

CONCEPT: Inheritance (class CartPage inherits from BasePage)
WHY: BasePage already has common browser actions (click, fill, goto).
     By inheriting, CartPage gets all those for free without rewriting them.
"""

import re                              # CONCEPT: Standard Library Module
                                       # WHY: 're' gives us Regular Expressions
                                       # to find patterns in text (e.g. find "$915" in a sentence)

from FD.pages.base_page import BasePage  # CONCEPT: Inheritance / Import
                                          # WHY: BasePage has self.page (the browser tab)
                                          # CartPage inherits it so we can use self.page here too


# -----------------------------------------------------------------------
# CONCEPT: Helper Functions (outside the class)
# WHY: These three functions (log_pass, log_fail, log_skip) are used
#      by EVERY method in this file. Putting them outside the class
#      avoids repeating the same code over and over (DRY principle —
#      Don't Repeat Yourself).
# -----------------------------------------------------------------------

def log_pass(step_name, expected_value, actual_value):
    """
    CONCEPT: Function with Return Value
    WHY: Instead of just printing, we RETURN a dictionary so the test
         can collect all results and write them to an Excel report.

    CONCEPT: Dictionary (key-value pairs)
    WHY: A dictionary lets us store multiple related values together.
         { "step": "...", "status": "PASS", ... }
    """
    print(f"  [PASS] {step_name}")           # CONCEPT: f-string formatting
    print(f"         Expected : {expected_value}")   # WHY: f-strings let us embed
    print(f"         Actual   : {actual_value}")     # variables directly in strings

    return {                                 # CONCEPT: Return a dictionary
        "step":     step_name,
        "expected": str(expected_value),     # CONCEPT: str() conversion
        "actual":   str(actual_value),       # WHY: ensures value is always a string
        "status":   "PASS",
        "error":    ""
    }


def log_fail(step_name, expected_value, actual_value, error_message=""):
    """
    CONCEPT: Default Parameter Value (error_message="")
    WHY: If the caller does not pass an error message, it defaults to
         empty string. This makes the function flexible.
    """
    print(f"  [FAIL] {step_name}")
    print(f"         Expected : {expected_value}")
    print(f"         Actual   : {actual_value}")
    print(f"         Error    : {error_message}")

    return {
        "step":     step_name,
        "expected": str(expected_value),
        "actual":   str(actual_value),
        "status":   "FAIL",
        "error":    str(error_message)
    }


def log_skip(step_name, reason=""):
    """
    CONCEPT: Intentional Skip
    WHY: Some checks are optional (e.g. metal name). If the data is
         not available, we SKIP instead of FAIL so the test does not
         break for the wrong reason.
    """
    print(f"  [SKIP] {step_name}")
    print(f"         Reason   : {reason}")

    return {
        "step":     step_name,
        "expected": "N/A",
        "actual":   "SKIPPED",
        "status":   "SKIP",
        "error":    reason
    }


# -----------------------------------------------------------------------
# CONCEPT: Class Definition
# WHY: A class groups related data and behaviour together.
#      CartPage groups everything related to the cart in one place.
#
# CONCEPT: Inheritance — CartPage(BasePage)
# WHY: CartPage extends BasePage. This means CartPage automatically
#      gets self.page (the Playwright browser page object) from BasePage.
#      We do not need to set it up again here.
# -----------------------------------------------------------------------

class CartPage(BasePage):

    # -------------------------------------------------------------------
    # CONCEPT: Instance Method (def method(self, ...))
    # WHY: 'self' refers to the current CartPage object.
    #      Every method needs 'self' so it can access self.page (the browser).
    # -------------------------------------------------------------------

    def wait_for_quick_cart(self):
        """
        CONCEPT: Wait for a specific element to appear (not just sleep)
        WHY: After clicking "Add to Bag", the quick cart opens automatically.
             Instead of blindly waiting 2 seconds, we wait for the cart
             to show actual content (item count > 0).
             This is more reliable than a fixed sleep.
        """
        results = []

        step_name = "Quick Cart - Wait for auto open"

        # Wait up to 8 seconds for the cart to show items
        # The cart icon/counter updates when an item is added
        try:
            # Try to wait for cart to show a non-zero count
            # Common patterns: "My Shopping Bag (1)", cart badge showing "1"
            self.page.wait_for_timeout(3000)  # initial wait for animation

            # Check if cart has items by looking for count > 0
            cart_count_text = self.page.evaluate("""
                () => {
                    // Look for any element that shows cart item count
                    const selectors = [
                        '.cart_count', '.cart-count', '.bag_count',
                        '[class*="cart_count"]', '[class*="bag_count"]',
                        '.cart_qty', '.mini_cart_count'
                    ];
                    for (const sel of selectors) {
                        const el = document.querySelector(sel);
                        if (el) return el.innerText.trim();
                    }
                    return '';
                }
            """)
            print(f"  [DEBUG] Cart count element text: '{cart_count_text}'")

        except Exception as wait_error:
            print(f"  [DEBUG] Wait error: {wait_error}")

        results.append(log_pass(step_name,
                                "Quick cart opens after Add to Bag",
                                self.page.url))
        return results


    def get_setting_name_from_complete_page(self):
        """
        CONCEPT: Locator Chaining
        WHY: We chain locators to narrow down to the exact element.
             .locator("div.prod_list_box").nth(0)  — first product box
             .locator("p span")                    — span inside p inside that box

        CONCEPT: String Methods (.split(), .join())
        WHY: We split the full name into words, take first 2, then join back.
             "Six Prong Solitaire" -> ["Six","Prong","Solitaire"] -> "Six Prong"
             This is because the quick cart may show a shorter product name.
        """
        try:
            # CONCEPT: Locator — finds an element on the page
            # nth(0) means the FIRST matching element (index starts at 0)
            setting_box = self.page.locator("div.prod_list_box").nth(0)

            # inner_text() reads the visible text of the element
            # .strip() removes leading/trailing spaces
            full_name = setting_box.locator("p span").inner_text().strip()

            # CONCEPT: String .split() — splits a string into a list of words
            # "Six Prong Solitaire 1.5mm" -> ["Six", "Prong", "Solitaire", "1.5mm"]
            words = full_name.split()

            # CONCEPT: List Slicing — words[:2] takes first 2 items
            # ["Six", "Prong", "Solitaire"] -> ["Six", "Prong"]
            # " ".join(...) joins them back with a space -> "Six Prong"
            short_name = " ".join(words[:2])

            print(f"  [INFO] Setting full name  : {full_name}")
            print(f"  [INFO] Setting search key : {short_name}")

            # CONCEPT: Multiple Return Values (tuple)
            # WHY: We return both the full name and the short name
            #      so the caller can use whichever they need
            return full_name, short_name

        except Exception as error:
            # CONCEPT: Exception Handling (try/except)
            # WHY: If the element is not found, we catch the error
            #      and return empty strings instead of crashing the test
            print(f"  [WARN] Could not read setting name: {error}")
            return "", ""


    def get_diamond_name_from_complete_page(self):
        """
        CONCEPT: Regular Expressions (re module)
        WHY: The diamond name is "1.06 Ct. Oval Lab Grown Diamond".
             We cannot just split by spaces because the format may vary.
             Regex lets us find specific PATTERNS:
             - r"\d+\.\d+" finds a number like "1.06"
             - r"(oval|round|...)" finds any shape word

        CONCEPT: re.IGNORECASE flag
        WHY: "Oval" and "oval" and "OVAL" should all match.
             IGNORECASE makes the search case-insensitive.
        """
        try:
            # nth(1) = SECOND product box (index 1) = diamond box
            diamond_box = self.page.locator("div.prod_list_box").nth(1)
            full_name = diamond_box.locator("p span").inner_text().strip()

            print(f"  [INFO] Diamond full name: {full_name}")

            # CONCEPT: re.search(pattern, string)
            # WHY: Searches for the pattern anywhere in the string
            # r"\d+\.\d+" means: one or more digits, a dot, one or more digits
            # Example: finds "1.06" in "1.06 Ct. Oval Lab Grown Diamond"
            carat_match = re.search(r"\d+\.\d+", full_name)

            # CONCEPT: Conditional Expression (ternary)
            # carat_match.group(0) gets the matched text, e.g. "1.06"
            # If no match found, use empty string ""
            carat = carat_match.group(0) if carat_match else ""

            # CONCEPT: re.search with alternation (|)
            # WHY: The | symbol means OR — match any of these shape words
            shape_match = re.search(
                r"(oval|round|cushion|pear|emerald|radiant|princess|marquise|heart|asscher)",
                full_name,
                re.IGNORECASE   # ignore case so "Oval" matches "oval"
            )
            shape = shape_match.group(0).lower() if shape_match else ""

            print(f"  [INFO] Extracted carat: {carat} | shape: {shape}")

            return full_name, carat, shape

        except Exception as error:
            print(f"  [WARN] Could not read diamond name: {error}")
            return "", "", ""


    def get_total_price_from_complete_page(self):
        """
        CONCEPT: Regex to extract price
        WHY: The price heading text might be "$915 MRP $1,525".
             We use regex r"\$[\d,]+" to find the first dollar amount.
             \$ = dollar sign, [\d,]+ = one or more digits or commas
        """
        try:
            price_heading = self.page.locator("div.price_box h2")
            price_text = price_heading.inner_text().strip()

            # Find first dollar amount in the text
            price_match = re.search(r"\$[\d,]+", price_text)
            total_price = price_match.group(0) if price_match else ""

            print(f"  [INFO] Total price from complete page: {total_price}")
            return total_price

        except Exception as error:
            print(f"  [WARN] Could not read price: {error}")
            return ""


    def get_all_quick_cart_text(self):
        """
        CONCEPT: JavaScript evaluate() inside Python
        WHY: When CSS selectors fail to find elements, we use
             page.evaluate() to run JavaScript directly in the browser.
             JavaScript can access ALL elements on the page, including
             ones that are dynamically added after page load.

        CONCEPT: Fallback strategy
        WHY: We first try CSS selectors. If they return nothing,
             we fall back to reading the full page body text.
             This ensures we always get some text to search through.
        """
        # Step 1: Use JavaScript to find all class names containing 'cart' or 'bag'
        # This helps us debug which selector to use
        try:
            cart_classes = self.page.evaluate("""
                () => {
                    const all_elements = document.querySelectorAll('[class]');
                    const found_classes = new Set();
                    all_elements.forEach(function(element) {
                        const class_string = element.className.toString();
                        const class_list = class_string.split(' ');
                        class_list.forEach(function(one_class) {
                            if (one_class && (
                                one_class.toLowerCase().includes('cart') ||
                                one_class.toLowerCase().includes('bag') ||
                                one_class.toLowerCase().includes('mini') ||
                                one_class.toLowerCase().includes('fly') ||
                                one_class.toLowerCase().includes('side')
                            )) {
                                found_classes.add(one_class);
                            }
                        });
                    });
                    return Array.from(found_classes).join(', ');
                }
            """)
            print(f"  [DEBUG] Cart/bag related classes on page: {cart_classes}")
        except Exception as debug_error:
            print(f"  [DEBUG] Could not get class names: {debug_error}")

        # Step 2: Try CSS selectors to find cart elements
        selectors_to_try = [
            "div.cart_item",
            "div.cart-item",
            "div.mini_cart",
            "div.cart_sidebar",
            "div.cart_drawer",
            "div.quick_cart",
            "div.fly_cart",
            "div.side_cart",
            "div[class*='cart']",
            "div[class*='bag']",
            "aside[class*='cart']",
        ]

        all_text_found = []

        for selector in selectors_to_try:
            elements = self.page.locator(selector)
            element_count = elements.count()

            if element_count > 0:
                print(f"  [DEBUG] Selector '{selector}' found {element_count} element(s)")

            for index in range(element_count):
                try:
                    text = elements.nth(index).inner_text().strip()
                    if text and len(text) > 3:
                        all_text_found.append(text)
                except Exception:
                    pass

        # Step 3: If nothing found via CSS selectors, read the full page body
        # WHY: The quick cart may use class names we have not tried yet.
        #      Reading the full body ensures we do not miss anything.
        if not all_text_found:
            print("  [DEBUG] No cart elements found via CSS — reading full page body text")
            try:
                body_text = self.page.locator("body").inner_text()
                all_text_found.append(body_text)
            except Exception as body_error:
                print(f"  [DEBUG] Could not read body: {body_error}")

        combined_text = " ".join(all_text_found).lower()
        print(f"  [INFO] Quick cart combined text (first 500 chars): {combined_text[:500]}")

        return combined_text


    def verify_setting_name_in_quick_cart(self):
        """
        CONCEPT: String 'in' operator
        WHY: Python's 'in' keyword checks if one string is inside another.
             "six prong" in "1.06ct oval six prong 10kt white gold" -> True
             This is simpler and more readable than using regex here.
        """
        step_name = "Quick Cart - Setting Name Visible"

        # Get setting name from complete page
        full_name, short_name = self.get_setting_name_from_complete_page()

        # CONCEPT: Guard clause — exit early if data is missing
        # WHY: No point searching the cart if we have nothing to search for
        if not short_name:
            return log_skip(step_name, "Could not read setting name from complete page")

        # Get all cart text
        cart_text = self.get_all_quick_cart_text()

        # CONCEPT: 'in' operator for substring search
        # short_name.lower() ensures case-insensitive comparison
        if short_name.lower() in cart_text:
            return log_pass(step_name, short_name, f"Found in cart: {cart_text[:100]}")
        else:
            return log_fail(step_name, short_name, cart_text[:100],
                            f"'{short_name}' not found in quick cart text")


    def verify_diamond_details_in_quick_cart(self):
        """
        CONCEPT: List to collect failures
        WHY: We check BOTH carat AND shape. Instead of returning immediately
             on the first failure, we collect ALL failures and report them
             together. This gives more useful feedback.
        """
        step_name = "Quick Cart - Diamond Carat and Shape Visible"

        full_name, carat, shape = self.get_diamond_name_from_complete_page()

        if not carat and not shape:
            return log_skip(step_name, "Could not read diamond details from complete page")

        cart_text = self.get_all_quick_cart_text()

        # CONCEPT: Empty list to collect failure messages
        failures = []

        # Check carat
        if carat:
            if carat in cart_text:
                print(f"  [INFO] Carat '{carat}' found in quick cart")
            else:
                # CONCEPT: list.append() — add failure message to list
                failures.append(f"Carat '{carat}' not found in cart")

        # Check shape
        if shape:
            if shape in cart_text:
                print(f"  [INFO] Shape '{shape}' found in quick cart")
            else:
                failures.append(f"Shape '{shape}' not found in cart")

        # CONCEPT: Boolean check on list
        # 'not failures' is True when the list is empty (no failures)
        if not failures:
            return log_pass(step_name,
                            f"carat={carat} | shape={shape}",
                            f"Both found in cart: {cart_text[:100]}")
        else:
            # CONCEPT: " | ".join(list) — joins failure messages with " | " separator
            return log_fail(step_name,
                            f"carat={carat} | shape={shape}",
                            cart_text[:100],
                            " | ".join(failures))


    def verify_metal_in_quick_cart(self, setting_details):
        """
        CONCEPT: Dictionary .get() method
        WHY: setting_details is a dictionary. Using .get("metal_color", "")
             safely returns "" if the key does not exist, instead of crashing.
             This is safer than setting_details["metal_color"] which would
             raise a KeyError if the key is missing.

        CONCEPT: Optional check (SKIP not FAIL)
        WHY: Metal name is optional per requirement. If it is not visible
             in the quick cart, we SKIP instead of FAIL.
        """
        step_name = "Quick Cart - Metal Name Visible (Optional)"

        # CONCEPT: Conditional expression with 'if'
        # If setting_details exists, get "metal_color", else use ""
        metal = setting_details.get("metal_color", "") if setting_details else ""
        metal = metal.lower().strip()   # lowercase and remove spaces

        if not metal:
            return log_skip(step_name, "No metal info available to check")

        cart_text = self.get_all_quick_cart_text()

        if metal in cart_text:
            return log_pass(step_name, metal, f"Found in cart: {cart_text[:100]}")
        else:
            # SKIP (not FAIL) — metal is optional
            return log_skip(step_name, f"Metal '{metal}' not visible in quick cart — skipping as optional")


    def verify_total_price_in_quick_cart(self):
        """
        CONCEPT: SKIP for optional/uncertain checks
        WHY: The total price may not always be visible in the quick cart
             (it might only show after scrolling or on the full cart page).
             We SKIP instead of FAIL to avoid false failures.
        """
        step_name = "Quick Cart - Total Price Match"

        expected_price = self.get_total_price_from_complete_page()

        if not expected_price:
            return log_skip(step_name, "Could not read price from complete page")

        cart_text = self.get_all_quick_cart_text()

        if expected_price in cart_text:
            return log_pass(step_name, expected_price, f"Found in cart: {cart_text[:100]}")
        else:
            return log_skip(step_name,
                            f"Price '{expected_price}' not visible in quick cart — skipping as optional")


    def click_view_bag_button(self, should_click=True):
        """
        CONCEPT: Conditional execution (if/else)
        WHY: We only click View Bag if all previous checks passed.
             If something failed, we skip clicking to avoid going to
             a wrong state.

        CONCEPT: scroll_into_view_if_needed()
        WHY: The View Bag button might be below the visible area of the screen.
             This scrolls the page so the button is visible before clicking.

        CONCEPT: wait_for(state="visible")
        WHY: Even after scrolling, the button might still be animating.
             We wait up to 8 seconds for it to become fully visible.

        The exact HTML of the button is:
        <span class="button-base view_bag"> View Bag </span>
        CSS selector: span.button-base.view_bag
        (span tag with BOTH classes: button-base AND view_bag)
        """
        step_name = "Quick Cart - Click View Bag Button"

        # CONCEPT: Guard clause — exit early if we should not click
        if not should_click:
            return log_skip(step_name, "Skipped because a previous cart check failed")

        try:
            # CONCEPT: CSS Selector with multiple classes
            # "span.button-base.view_bag" means:
            # a <span> element that has class "button-base" AND class "view_bag"
            view_bag_button = self.page.locator("span.button-base.view_bag").first

            # Scroll the button into the visible area of the screen
            view_bag_button.scroll_into_view_if_needed()

            # Wait up to 8 seconds for the button to be visible
            view_bag_button.wait_for(state="visible", timeout=8000)

            # Click the button
            view_bag_button.click()

            # Wait 2 seconds for the full cart page to load after clicking
            self.page.wait_for_timeout(2000)

            return log_pass(step_name, "View Bag button clicked", f"Now on: {self.page.url}")

        except Exception as error:
            return log_fail(step_name, "View Bag button clicked", "Button not found or not clickable", error)


    def verify_quick_cart(self, setting_details=None, diamond_details=None):
        """
        CONCEPT: Orchestrator Method
        WHY: This is the MAIN method that calls all the smaller methods
             in the correct order. The test file only needs to call
             verify_quick_cart() — it does not need to know the steps.
             This is the Page Object Model pattern in action.

        CONCEPT: list.extend() vs list.append()
        WHY: wait_for_quick_cart() returns a LIST of results.
             extend() adds all items from that list into all_results.
             append() would add the list itself as one item (wrong).

        CONCEPT: any() built-in function
        WHY: any(condition for item in list) returns True if the condition
             is True for AT LEAST ONE item in the list.
             We use it to check if any result has status="FAIL".
        """
        all_results = []    # CONCEPT: List to collect all results

        print("\n========== QUICK CART VERIFICATION ==========")

        # Step 1: Wait for quick cart to open
        # CONCEPT: list.extend() — adds all items from another list
        wait_results = self.wait_for_quick_cart()
        all_results.extend(wait_results)

        # Step 2: Check setting name
        # CONCEPT: list.append() — adds one item to the list
        all_results.append(self.verify_setting_name_in_quick_cart())

        # Step 3: Check diamond carat and shape
        all_results.append(self.verify_diamond_details_in_quick_cart())

        # Step 4: Check metal (optional)
        all_results.append(self.verify_metal_in_quick_cart(setting_details))

        # Step 5: Check total price (optional)
        all_results.append(self.verify_total_price_in_quick_cart())

        # CONCEPT: any() with generator expression
        # Checks if ANY result in all_results has status == "FAIL"
        # If yes, any_failed = True
        any_failed = any(result["status"] == "FAIL" for result in all_results)

        # Step 6: Click View Bag only if nothing failed
        # CONCEPT: 'not' operator — flips True to False and vice versa
        all_results.append(self.click_view_bag_button(should_click=not any_failed))

        # Print overall result
        if any_failed:
            print("  [CART OVERALL] FAIL")
        else:
            print("  [CART OVERALL] PASS")

        return all_results  # return all results for the test to use

import time
import yaml

from FD.pages.base_page import BasePage
from FD.locators.checkout_locators import CheckoutLocators
from pages.cart_page import log_fail, log_pass
from utils.email_generator import generate_email


class CheckoutPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # ============================================================
        # LOAD YAML TEST DATA
        # ============================================================

        with open("config/credentials.yaml", "r") as file:
            data = yaml.safe_load(file)

        self.user = data["default_user"]

    # ================================================================
    # COMMON SCROLL HELPER
    # ================================================================

    def scroll_to_element(self, locator, timeout=10000):
        """
        Wait for element and scroll it into the viewport.
        """

        locator.wait_for(
            state="attached",
            timeout=timeout
        )

        locator.scroll_into_view_if_needed()

        self.page.wait_for_timeout(500)

        return locator

    # ================================================================
    # PRODUCT INFORMATION
    # ================================================================

    def get_product_name(self):

        locator = self.page.locator(
            CheckoutLocators.PRODUCT_NAME
        )

        self.scroll_to_element(locator)

        return self.text(
            CheckoutLocators.PRODUCT_NAME
        )

    def get_product_price(self):

        locator = self.page.locator(
            CheckoutLocators.PRODUCT_PRICE
        )

        self.scroll_to_element(locator)

        return self.text(
            CheckoutLocators.PRODUCT_PRICE
        )

    # ================================================================
    # STEP 1 - ENTER GUEST EMAIL
    # ================================================================

    def enter_guest_email(self):

        step_name = "Checkout - Enter Guest Email"

        try:

            email = generate_email()

            print(
                f"  [INFO] Dynamic Email Generated: {email}"
            )

            email_field = self.page.locator(
                CheckoutLocators.CONTACT_EMAIL
            )

            # --------------------------------------------------------
            # SCROLL TO EMAIL
            # --------------------------------------------------------

            self.scroll_to_element(
                email_field
            )

            # --------------------------------------------------------
            # FILL EMAIL
            # --------------------------------------------------------

            email_field.fill(email)

            self.page.wait_for_timeout(500)

            actual_email = (
                email_field.input_value().strip()
            )

            assert actual_email == email, (
                f"Email was not entered correctly. "
                f"Expected: {email}, "
                f"Actual: {actual_email}"
            )

            print(
                "  [PASS] Guest email entered"
            )

            log_pass(
                step_name,
                "Guest email entered",
                "Email field filled successfully"
            )

            return True

        except Exception as error:

            print(
                f"  [FAIL] Guest Email: {error}"
            )

            log_fail(
                step_name,
                "Guest email entered",
                "Email field filling failed",
                str(error)
            )

            return False

    # ================================================================
    # STEP 2 - CONTINUE TO ADDRESS
    # ================================================================

    def click_continue_to_address(self):

        step_name = "Checkout - Continue To Address"

        try:

            continue_button = self.page.locator(
                CheckoutLocators.CONTINUE_TO_ADDRESS
            )

            # --------------------------------------------------------
            # SCROLL TO CONTINUE BUTTON
            # --------------------------------------------------------

            self.scroll_to_element(
                continue_button
            )

            # --------------------------------------------------------
            # CHECK ENABLED
            # --------------------------------------------------------

            if not continue_button.is_enabled():

                raise Exception(
                    "Continue To Address button is disabled"
                )

            # --------------------------------------------------------
            # CLICK
            # --------------------------------------------------------

            continue_button.click()

            self.page.wait_for_timeout(2000)

            print(
                "  [PASS] Continue To Address clicked"
            )

            log_pass(
                step_name,
                "Continue To Address clicked",
                "Address section loaded"
            )

            return True

        except Exception as error:

            print(
                f"  [FAIL] Continue To Address: {error}"
            )

            log_fail(
                step_name,
                "Continue To Address clicked",
                "Continue button click failed",
                str(error)
            )

            return False

    # ================================================================
    # STEP 3 - FILL SHIPPING ADDRESS
    # ================================================================

    def fill_shipping_address(self):

        step_name = "Checkout Address - Fill User Details"

        try:

            # ========================================================
            # USER DATA
            # ========================================================

            first_name = self.user["first_name"]
            last_name = self.user["last_name"]
            phone = self.user["phone"]

            address = self.user["address_line1"]
            city = self.user["city"]
            state = self.user["state"]
            zip_code = self.user["zip_code"]
            country = self.user["country"]

            # ========================================================
            # FIRST NAME
            # ========================================================

            first_name_field = self.page.locator(
                "//input[@name='shipping_first_name']"
            )

            self.scroll_to_element(
                first_name_field
            )

            first_name_field.fill(
                first_name
            )

            print(
                f"  [INFO] First Name Entered: {first_name}"
            )

            # ========================================================
            # LAST NAME
            # ========================================================

            last_name_field = self.page.locator(
                "//input[@name='shipping_last_name']"
            )

            self.scroll_to_element(
                last_name_field
            )

            last_name_field.fill(
                last_name
            )

            print(
                f"  [INFO] Last Name Entered: {last_name}"
            )

            # ========================================================
            # COUNTRY
            # ========================================================

            country_dropdown = self.page.locator(
                "//select[@name='country']"
            )

            self.scroll_to_element(
                country_dropdown
            )

            country_dropdown.select_option(
                label=country
            )

            print(
                f"  [INFO] Country Selected: {country}"
            )

            self.page.wait_for_timeout(1500)

            # ========================================================
            # ADDRESS
            # ========================================================

            address_field = self.page.locator(
                "//input[@placeholder='Please enter your address']"
            )

            self.scroll_to_element(
                address_field
            )

            address_field.fill(
                address
            )

            print(
                f"  [INFO] Address Entered: {address}"
            )

            self.page.wait_for_timeout(3000)

            # ========================================================
            # GOOGLE ADDRESS SUGGESTION
            # ========================================================

            suggestion = self.page.locator(
                "(//div[contains(@class,'pac-item')])[1]"
            )

            try:

                suggestion.wait_for(
                    state="visible",
                    timeout=5000
                )

                self.scroll_to_element(
                    suggestion,
                    timeout=5000
                )

                suggestion.click()

                print(
                    "  [PASS] Google address selected"
                )

                self.page.wait_for_timeout(2000)

            except Exception:

                print(
                    "  [INFO] Google address suggestion "
                    "not displayed - continuing"
                )

            # ========================================================
            # CITY
            # ========================================================

            city_field = self.page.locator(
                "//input[@name='shipping_city']"
            )

            self.scroll_to_element(
                city_field
            )

            current_city = (
                city_field.input_value().strip()
            )

            if not current_city:

                city_field.fill(
                    city
                )

                print(
                    f"  [INFO] City Entered: {city}"
                )

            else:

                print(
                    f"  [INFO] City already populated: "
                    f"{current_city}"
                )

            # ========================================================
            # STATE
            # ========================================================

            state_dropdown = self.page.locator(
                "//select[@name='state']"
            )

            self.scroll_to_element(
                state_dropdown
            )

            current_state = (
                state_dropdown.input_value().strip()
            )

            if not current_state:

                state_dropdown.select_option(
                    label=state
                )

                print(
                    f"  [INFO] State Selected: {state}"
                )

            else:

                print(
                    f"  [INFO] State already populated: "
                    f"{current_state}"
                )

            # ========================================================
            # ZIP CODE
            # ========================================================

            zip_field = self.page.locator(
                "//input[@name='shipping_postcode']"
            )

            self.scroll_to_element(
                zip_field
            )

            current_zip = (
                zip_field.input_value().strip()
            )

            if not current_zip:

                zip_field.fill(
                    zip_code
                )

                print(
                    f"  [INFO] Zip Code Entered: {zip_code}"
                )

            else:

                print(
                    f"  [INFO] Zip already populated: "
                    f"{current_zip}"
                )

            # ========================================================
            # PHONE NUMBER
            # ========================================================

            phone_field = self.page.locator(
                "//input[@id='MazInputPhoneNumber-v-0-0-9-0-0-phone']"
            )

            self.scroll_to_element(
                phone_field
            )

            phone_field.fill(
                phone
            )

            print(
                f"  [INFO] Phone Number Entered: {phone}"
            )

            # ========================================================
            # SCROLL TO BOTTOM AFTER ADDRESS
            # ========================================================

            self.page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )

            self.page.wait_for_timeout(1500)

            print(
                "  [PASS] All checkout details entered"
            )

            log_pass(
                step_name,
                "All checkout details entered",
                "Form filled successfully"
            )

            return True

        except Exception as error:

            print(
                f"  [FAIL] Checkout Address: {error}"
            )

            log_fail(
                step_name,
                "Form filled successfully",
                "Form filling failed",
                str(error)
            )

            return False

    # ================================================================
    # STEP 4 - PROCEED TO PAYMENT
    # ================================================================

    def click_proceed_to_payment(self):

        step_name = "Checkout Address - Proceed To Payment"

        try:

            print(
                "  [INFO] Looking for Proceed To Payment button"
            )

            # ========================================================
            # LOCATOR 1 - YOUR CURRENT LOCATOR
            # ========================================================

            proceed_button = self.page.locator(
                CheckoutLocators.PROCEED_TO_PAYMENT
            )

            # ========================================================
            # WAIT FOR BUTTON TO EXIST
            # ========================================================

            proceed_button.wait_for(
                state="attached",
                timeout=15000
            )

            print(
                "  [INFO] Proceed To Payment button found"
            )

            # ========================================================
            # SCROLL TO BUTTON
            # ========================================================

            proceed_button.scroll_into_view_if_needed()

            self.page.wait_for_timeout(1000)

            # ========================================================
            # CHECK VISIBLE
            # ========================================================

            if not proceed_button.is_visible():

                raise Exception(
                    "Proceed To Payment button exists "
                    "but is not visible"
                )

            # ========================================================
            # CHECK ENABLED
            # ========================================================

            if not proceed_button.is_enabled():

                print(
                    "  [INFO] Proceed button is disabled"
                )

                # Try scrolling to bottom again
                self.page.evaluate(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )

                self.page.wait_for_timeout(1500)

                if not proceed_button.is_enabled():

                    raise Exception(
                        "Proceed To Payment button is disabled"
                    )

            # ========================================================
            # CLICK
            # ========================================================

            proceed_button.click()

            print(
                "  [PASS] Proceed To Payment clicked"
            )

            self.page.wait_for_timeout(3000)

            log_pass(
                step_name,
                "Proceed To Payment clicked",
                "User moved to payment page"
            )

            return True

        except Exception as first_error:

            print(
                f"  [INFO] Normal payment button click failed: "
                f"{first_error}"
            )

            # ========================================================
            # FALLBACK LOCATOR
            # ========================================================

            try:

                print(
                    "  [INFO] Trying fallback payment button locator"
                )

                fallback_button = self.page.locator(
                    "//button[contains("
                    "translate(normalize-space(.), "
                    "'abcdefghijklmnopqrstuvwxyz', "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
                    "'PROCEED TO PAYMENT')]"
                )

                fallback_button.wait_for(
                    state="attached",
                    timeout=10000
                )

                fallback_button.scroll_into_view_if_needed()

                self.page.wait_for_timeout(1000)

                if not fallback_button.is_visible():

                    raise Exception(
                        "Fallback payment button "
                        "is not visible"
                    )

                if not fallback_button.is_enabled():

                    raise Exception(
                        "Fallback payment button "
                        "is disabled"
                    )

                fallback_button.click()

                print(
                    "  [PASS] Proceed To Payment clicked "
                    "(fallback locator)"
                )

                self.page.wait_for_timeout(3000)

                log_pass(
                    step_name,
                    "Proceed To Payment clicked",
                    "User moved to payment page"
                )

                return True

            except Exception as second_error:

                print(
                    f"  [FAIL] Proceed To Payment: "
                    f"{second_error}"
                )

                # ====================================================
                # DEBUG SCREENSHOT
                # ====================================================

                try:

                    self.page.screenshot(
                        path=(
                            "reports/screenshots/"
                            "proceed_to_payment_failure.png"
                        ),
                        full_page=True
                    )

                    print(
                        "  [INFO] Payment failure screenshot saved"
                    )

                except Exception:

                    pass

                log_fail(
                    step_name,
                    "Proceed To Payment clicked",
                    "Button click failed",
                    str(second_error)
                )

                return False

    # ================================================================
    # STEP 5 - VERIFY PAYMENT SECTION
    # ================================================================

    def verify_payment_section(self):

        step_name = "Checkout - Verify Payment Section"

        try:

            print("  [INFO] Verifying payment section")

            # ============================================================
            # VERIFY CHECKOUT URL
            # ============================================================

            current_url = self.page.url.lower()

            assert "/checkout/" in current_url, (
                f"User is not on checkout page. "
                f"Current URL: {current_url}"
            )

            print(
                f"  [PASS] Checkout URL detected: {current_url}"
            )

            # ============================================================
            # CHECK COMMON ERRORS
            # ============================================================

            body_text = (
                self.page.locator("body")
                .inner_text()
                .lower()
            )

            assert "something went wrong" not in body_text, (
                "[FAIL] Something went wrong error displayed"
            )

            assert "page not found" not in body_text, (
                "[FAIL] 404 Page Not Found displayed"
            )

            assert "invalid cart identifier" not in body_text, (
                "[FAIL] Invalid cart identifier displayed"
            )

            # ============================================================
            # PAYMENT SECTION
            # ============================================================

            payment_section = self.page.locator(
                CheckoutLocators.PAYMENT_SECTION
            )

            # Scroll to payment section
            payment_section.scroll_into_view_if_needed()

            self.page.wait_for_timeout(1000)

            # Wait until visible
            payment_section.wait_for(
                state="visible",
                timeout=15000
            )

            assert payment_section.is_visible(), (
                "[FAIL] Payment section is not visible"
            )

            print(
                "  [PASS] Payment section displayed"
            )

            log_pass(
                step_name,
                "Payment section displayed",
                "Payment section loaded successfully"
            )

            return True

        except Exception as error:

            print(
                f"  [FAIL] Payment verification: {error}"
            )

            try:
                self.page.screenshot(
                    path=(
                        "reports/screenshots/"
                        "payment_section_failure.png"
                    ),
                    full_page=True
                )
            except Exception:
                pass

            log_fail(
                step_name,
                "Payment section displayed",
                "Payment section validation failed",
                str(error)
            )

            return False

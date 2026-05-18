from FD.pages.base_page import BasePage
from FD.pages.cart_page import log_fail, log_pass, log_skip
from FD.utils.email_generator import generate_email

from playwright.sync_api import TimeoutError
import yaml


class CheckoutAddress(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # ============================================================
        # LOAD YAML TEST DATA
        # ============================================================

        with open("FD/config/credentials.yaml", "r") as file:
            data = yaml.safe_load(file)

        self.user = data["default_user"]

    # ============================================================
    # VERIFY PAGE TITLE
    # ============================================================

    def verify_title(self):

        step_name = "Checkout Address - Page Title"

        try:

            heading = self.page.locator("//h3[contains(text(),'My Details')]")
            heading.wait_for(state="visible", timeout=15000)

            full_text = heading.inner_text().strip()

            if "my details" in full_text.lower():

                print(f"[PASS] {step_name}")
                print(f"Expected: My Details")
                print(f"Actual  : {full_text}")

                return log_pass(step_name, "My Details", full_text)

            else:

                print(f"[FAIL] {step_name}")
                print(f"Expected: My Details")
                print(f"Actual  : {full_text}")

                return log_fail(step_name, "My Details", full_text, "Mismatch")

        except Exception as error:

            print(f"[FAIL] {step_name}")
            print(f"Expected: My Details")
            print(f"Actual  : Not Found")

            return log_fail(step_name, "My Details visible", "Not found", str(error))

    # ============================================================
    # DISMISS OFFER MODAL
    # ============================================================

    def dismiss_modal(self):

        step_name = "Checkout Address - Dismiss Popup"

        try:

            close_button = self.page.locator(
                "(//a[normalize-space()='X'])[1]"
            ).first

            close_button.wait_for(
                state="visible",
                timeout=5000
            )

            close_button.click()

            self.page.wait_for_timeout(1000)

            print("  [PASS] Offer popup dismissed")

            return log_pass(
                step_name,
                "Popup closed",
                "Popup dismissed"
            )

        except TimeoutError:

            print("  [SKIP] Popup not displayed")

            return log_skip(
                step_name,
                "Popup not displayed"
            )

        except Exception as error:

            print(f"  [FAIL] {error}")

            return log_fail(
                step_name,
                "Popup closed",
                "Popup not closed",
                str(error)
            )

    # ============================================================
    # CREATE ACCOUNT + FILL ADDRESS DETAILS
    # ============================================================

    def create_account_and_fill_details(self):

        step_name = "Checkout Address - Fill User Details"

        try:

            # ====================================================
            # USER DATA
            # ====================================================

            first_name = self.user["first_name"]
            last_name = self.user["last_name"]

            # ====================================================
            # DYNAMIC EMAIL
            # ====================================================

            email = generate_email()

            print(f"  [INFO] Dynamic Email Generated : {email}")

            phone = self.user["phone"]

            address = self.user["address_line1"]
            city = self.user["city"]
            state = self.user["state"]
            zip_code = self.user["zip_code"]
            country = self.user["country"]

            # ====================================================
            # ACCOUNT DETAILS
            # ====================================================

            self.page.locator(
                "//input[@id='first_name']"
            ).fill(first_name)

            self.page.locator(
                "//input[@id='last_name']"
            ).fill(last_name)

            self.page.locator(
                "//input[@id='email']"
            ).fill(email)

            # ====================================================
            # CREATE ACCOUNT CHECKBOX
            # ====================================================

            create_account_checkbox = self.page.locator(
                "//span[@class='unchecked']"
            )

            create_account_checkbox.click()

            self.page.wait_for_timeout(1000)

            # ====================================================
            # PASSWORD = EMAIL
            # ====================================================

            self.page.locator(
                "//input[@id='password']"
            ).fill(email)

            self.page.locator(
                "//input[@id='confirm_password']"
            ).fill(email)

            # ====================================================
            # SHIPPING DETAILS
            # ====================================================

            self.page.locator(
                "//input[@name='shipping_first_name']"
            ).fill(first_name)

            self.page.locator(
                "//input[@name='shipping_last_name']"
            ).fill(last_name)

            # ====================================================
            # COUNTRY DROPDOWN
            # ====================================================

            country_dropdown = self.page.locator(
                "//select[@name='country']"
            )

            country_dropdown.select_option(
                label=country
            )

            print(f"  [INFO] Country Selected : {country}")

            self.page.wait_for_timeout(1500)

            # ====================================================
            # ADDRESS FIELD
            # ====================================================

            address_field = self.page.locator(
                "//input[@placeholder='Please enter your address']"
            )

            address_field.fill(address)

            self.page.wait_for_timeout(3000)

            # ====================================================
            # GOOGLE ADDRESS SUGGESTION
            # ====================================================

            suggestion = self.page.locator(
                "(//div[contains(@class,'pac-item')])[1]"
            )

            try:

                suggestion.wait_for(
                    state="visible",
                    timeout=5000
                )

                suggestion.click()

                print("  [PASS] Google address selected")

                self.page.wait_for_timeout(3000)

            except Exception:

                print("  [INFO] Google suggestion not displayed")

            # ====================================================
            # CITY
            # ====================================================

            city_field = self.page.locator(
                "//input[@name='shipping_city']"
            )

            current_city = city_field.input_value().strip()

            if current_city == "":

                city_field.fill(city)

                print(f"  [INFO] City Entered : {city}")

            # ====================================================
            # STATE
            # ====================================================

            state_dropdown = self.page.locator(
                "//select[@name='state']"
            )

            current_state = state_dropdown.input_value().strip()

            if current_state == "":

                state_dropdown.select_option(
                    label=state
                )

                print(f"  [INFO] State Selected : {state}")

            # ====================================================
            # ZIP CODE
            # ====================================================

            zip_field = self.page.locator(
                "//input[@name='shipping_postcode']"
            )

            current_zip = zip_field.input_value().strip()

            if current_zip == "":

                zip_field.fill(zip_code)

                print(f"  [INFO] Zip Code Entered : {zip_code}")

            # ====================================================
            # PHONE NUMBER
            # ====================================================

            phone_field = self.page.locator(
                "//input[@name='shipping_phone']"
            )

            phone_field.fill(phone)

            print(f"  [INFO] Phone Number Entered : {phone}")

            # ====================================================
            # WAIT BEFORE CONTINUE
            # ====================================================

            self.page.wait_for_timeout(2000)

            print("  [PASS] All checkout details entered")

            return log_pass(
                step_name,
                "All checkout details entered",
                "Form filled successfully"
            )

        except Exception as error:

            print(f"  [FAIL] {error}")

            return log_fail(
                step_name,
                "Form filled successfully",
                "Form filling failed",
                str(error)
            )

    # ============================================================
    # CLICK PROCEED TO PAYMENT
    # ============================================================

    def click_proceed_to_payment(self):

        step_name = "Checkout Address - Proceed To Payment"

        try:

            proceed_button = self.page.locator(
                "//button//span[contains(text(),'PROCEED TO PAYMENT')]"
            )

            proceed_button.scroll_into_view_if_needed()
            self.page.wait_for_timeout(1000)
            proceed_button.click()

            self.page.wait_for_load_state("networkidle")

            print("  [PASS] Proceed To Payment clicked")

            return log_pass(
                step_name,
                "Proceed To Payment clicked",
                "User moved to payment page"
            )

        except Exception as error:

            print(f"  [FAIL] {error}")

            return log_fail(
                step_name,
                "Proceed To Payment clicked",
                "Button click failed",
                str(error)
            )
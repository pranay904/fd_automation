from playwright.sync_api import expect

from pages.base_page import BasePage

class BaseFormPage(BasePage):

    # -------- common fields --------
    def fill_name(self, value):
        locator = self.page.locator("(//input[@name='name'])[1]")
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(value)

    def fill_name_jewelry(self, value):
        locator = self.page.locator("(//input[@name='name'])[1]")
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(value)

    def fill_first_name(self, value):
        locator = self.page.locator("input[name='first_name']")
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(value)

    def fill_last_name(self, value):
        locator = self.page.locator("input[name='last_name']']")
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(value)


    def fill_email_contact(self, value):
        locator = self.page.locator("(//input[@name='email'])")
        expect(locator).to_be_visible(timeout=5000)  # wait up to 5s
        locator.fill(value)

    def fill_email(self, value):
        locator = self.page.locator("(//input[@name='email'])[2]")
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(value)

    def fill_phone(self, value):
        locator = self.page.locator("(//input[@name='phone'])[1]")
        expect(locator).to_be_visible(timeout=5000)  # wait up to 5s
        locator.fill(value)

    def fill_message(self, value):
        self.fill("(//textarea[@name='message'])[1]", value)


    # -------- file upload --------
    def upload_file(self, upload_button_selector, file_input_selector, file_path):
        # Step 1: Click the Upload Media button to reveal the file input
        self.page.click(upload_button_selector)

        # Step 2: Wait for the file input to be visible
        file_input = self.page.locator(file_input_selector)
        expect(file_input).to_be_visible(timeout=5000)

        # Step 3: Upload the file
        file_input.set_input_files(file_path)

    # -------- submit --------
    def submit_form(self, selector="button[type='submit']"):
        self.click(selector)


    def send(self):
        # Click submit
        submit_btn = self.page.locator("button[type='submit']")
        expect(submit_btn).to_be_enabled(timeout=5000)
        submit_btn.click()

        # --- wait for confirmation ---
        # Example: wait for success message
        success_msg = self.page.locator("//div[contains(text(),'Thank you')]")
        expect(success_msg).to_be_visible(timeout=5000)


    def select_jewelry_type(self):

        jewelry_tye = self.page.locator("(//div[@class='current_active'])[1]")
        jewelry_tye.click()
        options = self.page.locator("//span[normalize-space()='Pendants']")
        options.click()

    def select_budget_type(self):
        budget_dropdown = self.page.locator("(//div[@class='current_active'])[2]")
        budget_dropdown.click()

        # Wait for the "$2,000 - $3,000" option visible
        budget_option = self.page.locator("span:has-text('$2,000 - $3,000')")
        budget_option.wait_for(state="visible")
        budget_option.click()


    # -------- Drop a Hint specific fields --------
    DROP_HINT_NAME = "//input[@name='name']"
    DROP_HINT_EMAIL = "//div[@class='col-md-12 pb-3 column']//input[@name='email']"
    DROP_HINT_PARTNER_NAME = "//input[@name='partners_name']"
    DROP_HINT_PARTNER_EMAIL = "//input[@name='partners_email']"
    DROP_HINT_MESSAGE = "(//textarea[@name='message'])[1]"
    DROP_HINT_SUBMIT = "//button[normalize-space()='submit']"

    # -------- Drop a Hint full form method --------
    def drop_hint_all_fields(self, name, email, partner_name, partner_email, message,):
        # Fill Drop a Hint fields
        locator = self.page.locator(self.DROP_HINT_NAME)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(name)

        locator = self.page.locator(self.DROP_HINT_EMAIL)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(email)

        locator = self.page.locator(self.DROP_HINT_PARTNER_NAME)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(partner_name)

        locator = self.page.locator(self.DROP_HINT_PARTNER_EMAIL)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(partner_email)

        locator = self.page.locator(self.DROP_HINT_MESSAGE)
        expect(locator).to_be_visible(timeout=5000)
        locator.fill(message)

    def submit_gemo_drop_hint_form(self):
        submit_btn = self.page.locator("button:has-text('Submit')")  # replace with actual locator
        expect(submit_btn).to_be_enabled(timeout=5000)  # wait until button is clickable
        submit_btn.click()














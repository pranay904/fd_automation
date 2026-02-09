import time

from playwright.sync_api import expect

from utils.email_generator import generate_email
from utils.json_reader import read_json_file, file_path
from utils.config import REGISTER_URL, LOGIN_URL

class RegisterPage:
    def __init__(self, page):
        self.page = page
        self.email = generate_email()
        self.data = read_json_file(file_path)

        # Update login_user in memory for login test
        self.data["login_user"]["email"] = self.email
        self.data["login_user"]["password"] = self.email  # password = email

    def close_popup_if_present(self):
        popup = self.page.locator('div.content_container:visible')
        if popup.is_visible():
            expect(popup).not_to_be_visible(timeout=5000)
        self.page.locator("svg[width='24']").click()

    # ---------------- Registration ----------------
    def open_register_page(self):
        """Navigate to the registration page"""
        self.page.goto(REGISTER_URL)

    def register_user(self):
        """Fill registration form and submit"""
        self.page.locator("//input[@name='first_name']").fill(self.data["register_user"]["firstName"])
        self.page.locator("//input[@name='last_name']").fill(self.data["register_user"]["lastName"])
        self.page.locator("div[class='col-md-12 pb-4 column'] input[name='email']").fill(self.email)
        self.page.locator("div.col-md-6.pb-4.column input[name='password']").fill(self.email)
        self.page.locator("input[name='password_confirmation']").fill(self.email)

        self.page.locator("//span[normalize-space()='Sign Up']").click()
        self.page.wait_for_timeout(10000)



        return self.email  # Return email for login test

    # ---------------- Logout ----------------
    def logout_user(self, hasText=None):
        """Click profile and logout"""
       
        # Open profile dropdown
        profile = self.page.locator("div.my_account")
        profile.wait_for(state="visible", timeout=15000)

        # 5️ Hover profile to open dropdown (use real mouse move for reliability)
        box = profile.bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        self.page.wait_for_timeout(300)  # wait for animation

        # 6️ Click "Personal Details"
        personal_details = self.page.locator("//li[normalize-space()='Personal Details']")
        personal_details.wait_for(state="visible", timeout=5000)
        personal_details.click()

        # Click logout
        self.page.locator("li", has_text="Logout").click()
        self.page.wait_for_timeout(2000)

    def open_login_page(self):
        self.page.goto(LOGIN_URL)
    # ---------------- Login ----------------
    def login_user(self):
        """Login using the same credentials"""
        self.page.goto(LOGIN_URL)
        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div input[name='email']").fill(self.data["login_user"]["email"])
        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div form div[class='row'] div[class='col-md-12'] div input[name='password']").fill(self.data["login_user"]["password"])
        self.page.get_by_role("button", name="LOGIN").click()
        self.page.wait_for_timeout(3000)


        # Verify login success by checking heading

        expect(self.page.locator("h1")).to_have_text("My account")



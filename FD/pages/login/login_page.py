from playwright.sync_api import expect

from FD.utils.json_reader import read_json_file, file_path
from FD.utils.config import LOGIN_URL

class LoginPage:



    def __init__(self, page):
        self.page = page
        self.data = read_json_file(file_path)  # reads the fixed JSON

    def open_login_page(self):
        self.page.goto(LOGIN_URL)


    def login_user(self):
        email = self.data["login_user"]["email"]
        password = self.data["login_user"]["password"]

        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div input[name='email']").fill(email)
        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div form div[class='row'] div[class='col-md-12'] div input[name='password']").fill(password)
        self.page.get_by_role("button", name="LOGIN").click()
        self.page.wait_for_timeout(5000)

        expect(
            self.page.get_by_role("heading", name="My account")
        ).to_have_text("My account")

    def login_with_credentials(self, email: str, password: str):
        """Login with given email and password — used by TC-002."""
        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div input[name='email']").fill(email)
        self.page.locator("div[class='col-md-6 col-lg-5 mx-auto'] div form div[class='row'] div[class='col-md-12'] div input[name='password']").fill(password)
        self.page.locator(
            "div[class='col-md-6 col-lg-5 mx-auto'] button[type='submit']"
        ).click()
        self.page.wait_for_timeout(5000)
        print(f"[INFO] Logged in as {email}")

    def login_cart_modal(self, email: str, password: str):
        """Login using cart page login modal."""

        # Login modal
        modal = self.page.locator("div.modal_body.modal_sm")
        modal.wait_for(state="visible", timeout=10000)

        # Email
        email_input = modal.locator("input[name='email']")
        email_input.wait_for(state="visible", timeout=10000)
        email_input.fill(email)

        # Password
        password_input = modal.locator("input[name='password']")
        password_input.wait_for(state="visible", timeout=10000)
        password_input.fill(password)

        # Login button
        login_btn = modal.locator("button[type='submit']")
        login_btn.wait_for(state="visible", timeout=10000)
        login_btn.click()

        print(f"[INFO] Logged in as {email} from cart modal.")



    def close_popup_if_present(self):
        pass



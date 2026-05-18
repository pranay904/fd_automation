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

    def close_popup_if_present(self):
        pass



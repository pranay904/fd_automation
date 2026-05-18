from OMS.utils.config import BASE_LOCAL

class LoginPage:
    def __init__(self, page):
        self.page = page
        # Locators using Playwright Python methods
        self.username_input = self.page.get_by_label('Email Address')
        self.password_input = self.page.get_by_label('Password')
        self.login_button = self.page.locator("//button[@type='submit']")

    def open_login_page(self):
        """Open the login URL and wait for page to load"""
        self.page.goto(BASE_LOCAL)
        # Wait until the URL contains "/login"
        self.page.wait_for_url("**/login", timeout=10000)
        # Wait for the username field to be visible
        self.username_input.wait_for(state="visible", timeout=10000)

    def login(self, email, password):
        """Fill login form and click login"""
        # Fill username
        self.username_input.fill(email)
        self.username_input.wait_for(state="visible", timeout=10000)
        # Fill password
        self.password_input.fill(password)
        self.username_input.wait_for(state="visible", timeout=10000)
        # Click login button
        self.login_button.click()
        self.username_input.wait_for(state="visible", timeout=10000)
        # Wait until the next page is fully loaded
        self.page.wait_for_load_state("networkidle")

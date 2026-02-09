import time

from utils.config import BASE_URL
from utils.email_generator import generate_email
from pages import register_page

class Guest:
    def __init__(self, page ):
        self.page= page


    def open_Base_url(self):
        self.page.goto(BASE_URL)

    def CYO_Ring(self):
        cyo_button = self.page.locator("(//span[contains(text(),'CREATE YOUR OWN')])[1]")

        # Wait for button to appear
       # cyo_button.wait_for(state="visible", timeout=30000)

        # Scroll into view (optional)
        cyo_button.scroll_into_view_if_needed()

        # Click safely
        cyo_button.click(force=True)
        time.sleep(2)

    def Shop(self):
        # with self.page.expect_navigation(wait_until="load"):
        shop = self.page.locator("(//span[contains(text(),'SHOP Fine jewelry')])[1]")
        shop.click()
        time.sleep(2)

        # self.page.go_back(wait_until="load")

    def RTS(self):
        # with self.page.expect_navigation(wait_until="load"):
        rts = self.page.locator("(//span[contains(text(),'SHOP IN-STOCK')])[1]")
        rts.click()
        time.sleep(2)


























from FD.pages.base_page import BasePage
from FD.locators.home_locators import HomeLocators
from FD.utils.config import BASE_URL, ETERNITY_RING, TWO_STONE, FIVE_STONE


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    def open_home(self):
        self.open_url(BASE_URL)

    def go_to_listing(self, listing_type="ETERNITY"):
        listing_type = listing_type.upper()
        if listing_type == "ETERNITY":
            self.open_url(ETERNITY_RING)
        elif listing_type == "TWO_STONE":
            self.open_url(TWO_STONE)
        elif listing_type == "FIVE_STONE":
            self.open_url(FIVE_STONE)
        else:
            raise ValueError(f"Invalid listing type: {listing_type}")

    def get_cart_badge(self):
        badge = self.text(HomeLocators.CART_BADGE)
        if badge.strip() == "":
            return 0
        return int(badge)

    def logout(self):
        """
        Hover on the account icon to open the dropdown, then click logout.
        Skips silently if user is not logged in.
        """
        try:
            # Hover the account/profile icon to reveal dropdown
            account_icon = self.page.locator("//div[contains(@class,'toggle_user')]")
            account_icon.wait_for(state="visible", timeout=5000)
            account_icon.hover()
            self.page.wait_for_timeout(600)

            # Click the logout li inside the dropdown
            logout_link = self.page.locator("//li[normalize-space()='logout']")
            logout_link.wait_for(state="visible", timeout=5000)
            logout_link.click()
            self.page.wait_for_load_state("load")
            print("[INFO] Logged out successfully")
        except Exception:
            print("[INFO] Not logged in — skipping logout")

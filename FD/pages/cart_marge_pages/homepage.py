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
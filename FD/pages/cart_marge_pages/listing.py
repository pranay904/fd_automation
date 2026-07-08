from playwright.sync_api import Page

from FD.pages.base_page import BasePage
from FD.locators.listing_locators import ListingLocators
from FD.utils.config import ETERNITY_RING
from locators.home_locators import HomeLocators
from utils.cart_count import CartCount


class Listing(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_count = CartCount(page)

        self.eternity_product_name = ""
        self.eternity_product_price = ""
        self.eternity_product_mrp = ""

    def open_url_eternity(self):
        self.open_url(ETERNITY_RING)


    def get_eternity_first_product_details(self):

        self.eternity_product_name = self.page.locator(
            ListingLocators.FIRST_PRODUCT_NAME
        ).text_content().strip()

        self.eternity_product_price = self.page.locator(
            ListingLocators.FIRST_PRODUCT_PRICE
        ).text_content().strip()

        self.eternity_product_mrp = self.page.locator(
            ListingLocators.FIRST_PRODUCT_MRP
        ).text_content().strip()

        print(f"Product Name : {self.eternity_product_name}")
        print(f"Product Price: {self.eternity_product_price}")
        print(f"Product MRP  : {self.eternity_product_mrp}")

    def select_first_eternity_product(self):
        self.click(ListingLocators.FIRST_PRODUCT)

    def open_first_product(self):
        """Wait for listing to load then click the first product name link."""
        el = self.page.locator(ListingLocators.FIRST_PRODUCT)
        el.wait_for(state="visible", timeout=15000)
        el.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)
        el.click()
        self.page.wait_for_load_state("load")
        # Wait for PDP h1 to confirm navigation succeeded
        self.page.wait_for_selector("//h1", timeout=20000)
        print("[INFO] Opened first product from listing")

    def get_listing_cart_count(self):
        return self.cart_count.get_listing_cart_count(
            HomeLocators.CART_BADGE
        )
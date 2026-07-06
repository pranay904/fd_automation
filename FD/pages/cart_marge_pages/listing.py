from playwright.sync_api import Page
from FD.pages.base_page import BasePage
from FD.utils.config import ETERNITY_RING
from locators.listing_locators import ListingLocators


class CartListing(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.product_name = ""
        self.product_price = ""
        self.product_mrp = ""

    def open_url_eternity(self):
        self.open_url(ETERNITY_RING)

    def Select_first_product(self):
        # Store product details
        self.product_name = self.page.locator(
            ListingLocators.FIRST_PRODUCT_NAME
        ).text_content().strip()

        self.product_price = self.page.locator(
            ListingLocators.FIRST_PRODUCT_PRICE
        ).text_content().strip()

        self.product_mrp = self.page.locator(
            ListingLocators.FIRST_PRODUCT_MRP
        ).text_content().strip()

        print(f"Product Name : {self.product_name}")
        print(f"Product Price: {self.product_price}")
        print(f"Product MRP  : {self.product_mrp}")

        # Click first product
        self.click(ListingLocators.FIRST_PRODUCT)
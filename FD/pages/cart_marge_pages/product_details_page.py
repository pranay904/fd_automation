from playwright.sync_api import Page

from FD.pages.base_page import BasePage
from FD.locators.product_locators import ProductLocators
from pages.cart_marge_pages.select_ring_size import SelectRingSize


class ProductDetailsPage(BasePage, SelectRingSize):

    def __init__(self, page: Page):
        super().__init__(page)

        self.eternity_product_name = ""
        self.eternity_product_price = ""
        self.eternity_product_mrp = ""

        self.complete_product_data = {}

    def verify_eternity_pdp_loaded(self):
        self.wait_for_element(ProductLocators.PRODUCT_NAME)

    def get_eternity_product_details(self):

        self.eternity_product_name = self.page.locator(
            ProductLocators.PRODUCT_NAME
        ).text_content().strip()

        self.eternity_product_price = self.page.locator(
            ProductLocators.PRODUCT_PRICE
        ).text_content().strip()

        self.eternity_product_mrp = self.page.locator(
            ProductLocators.PRODUCT_MRP
        ).text_content().strip()

        print(f"Eternity PDP Name : {self.eternity_product_name}")
        print(f"Eternity PDP Price: {self.eternity_product_price}")
        print(f"Eternity PDP MRP  : {self.eternity_product_mrp}")

    def verify_eternity_product_name(self, expected_name):
        actual_name = self.page.locator(
            ProductLocators.PRODUCT_NAME
        ).text_content().strip()

        assert actual_name == expected_name

    def verify_eternity_product_price(self, expected_price):
        actual_price = self.page.locator(
            ProductLocators.PRODUCT_PRICE
        ).text_content().strip()

        assert actual_price == expected_price

    def add_eternity_product_to_cart(self):
        # Select Ring Size before Add to Cart
        self.select_ring_size()

        # Click Add to Cart
        self.click(ProductLocators.ADD_TO_CART)


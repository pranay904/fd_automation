

from FD.pages.base_page import BasePage
from FD.locators.checkout_locators import CheckoutLocators


class CheckoutPage(BasePage):

    def get_product_name(self):
        return self.text(CheckoutLocators.PRODUCT_NAME)

    def get_product_price(self):
        return self.text(CheckoutLocators.PRODUCT_PRICE)
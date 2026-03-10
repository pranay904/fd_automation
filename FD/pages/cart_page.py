# pages/cart_page.py
from FD.pages.base_page import BasePage

class CartPage(BasePage):
    def verify_total_price(self, expected_price: str):
        """Verify that the total price in the cart matches the expected price."""
        total_price = self.page.locator("//span[@class='total-price']").text_content()
        assert expected_price == total_price, f"Total price mismatch: {expected_price} != {total_price}"

    def add_to_bag(self):
        """Click on the 'Add to Bag' button."""
        add_to_bag_button = self.page.locator("//button[contains(text(),'Add to Bag')]")
        self.scroll_into_view(add_to_bag_button)
        add_to_bag_button.click()

from playwright.sync_api import Page, expect
import time

class CYOSettingDetailsPage:
    def __init__(self, page: Page):
        self.page = page

    def verify_product_details(self, expected_details: dict):
        """Verify the product details on the setting details page."""

        # Extract the price from the details page
        price = self.page.locator("h4").inner_text().strip()
        expect(price).to_be(expected_details["price"], f"Price does not match! Expected: {expected_details['price']}, Found: {price}")

        # Extract the MRP (strikethrough price) from the details page
        mrp = self.page.locator("h4 .plp_mrp_box").inner_text().strip()
        expect(mrp).to_be(expected_details["mrp"], f"MRP does not match! Expected: {expected_details['mrp']}, Found: {mrp}")

        # Extract the product name from the details page (h3)
        product_name = self.page.locator("h3").inner_text().strip()
        expect(product_name).to_be(expected_details["product_name"], f"Product name does not match! Expected: {expected_details['product_name']}, Found: {product_name}")

        # Extract the active metal color (can vary, but we assume 'active' class marks the selected color)
        active_metal_color = self.page.locator(".metal_box.active").inner_text().strip()
        expect(active_metal_color).to_be(expected_details["metal_color"], f"Active metal color does not match! Expected: {expected_details['metal_color']}, Found: {active_metal_color}")

    def get_product_details(self):
        """Extract product details (price, MRP, product name, metal color) from the details page."""

        # Extract price
        price = self.page.locator("h4").inner_text().strip()

        # Extract MRP (strikethrough price)
        mrp = self.page.locator("h4 .plp_mrp_box").inner_text().strip()

        # Extract product name (h3)
        product_name = self.page.locator("h3").inner_text().strip()

        # Extract active metal color
        metal_color = self.page.locator(".metal_box.active").inner_text().strip()

        return {
            "price": price,
            "mrp": mrp,
            "product_name": product_name,
            "metal_color": metal_color
        }

    def select_this_setting(self):
        """Click on the 'SELECT THIS SETTING' button."""
        select_button = self.page.locator(':text("SELECT THIS SETTING")')
        self.page.scroll_into_view(select_button)
        select_button.click()
        time.sleep(2)  # Wait for navigation, or replace with appropriate wait


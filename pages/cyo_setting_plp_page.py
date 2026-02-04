from playwright.sync_api import Page, expect
import time


class CYOSettingPLPPage:
    def __init__(self, page: Page):
        self.page = page

    def go_to(self):
        """Navigate to the CYO Ring Settings PLP page."""
        self.page.goto("https://payment.ap-diam.com/ring-settings")

    def get_product_details(self):
        """Extract details like price, MRP, product name, and active metal color from the second product."""

        # Hardcode the locator to always select the second product
        product_locator = self.page.locator("(//div[@class='product_box'])[2]")  # Selects the second product

        # Wait for the product details container to be visible
        product_locator.wait_for(state="visible", timeout=10000)  # Increased timeout to 10 seconds

        # Wait for the price element inside the product box to be visible
        price_locator = product_locator.locator(".price h4")
        price_locator.wait_for(state="visible", timeout=5000)  # Wait for price to appear

        # Extract price text
        price = price_locator.inner_text()

        # Extract MRP (if available)
        mrp_locator = product_locator.locator(".plp_mrp_box")
        mrp_locator.wait_for(state="visible", timeout=5000)  # Wait for MRP to appear if available
        mrp = mrp_locator.inner_text() if mrp_locator.count() > 0 else None  # Check if MRP exists

        # Extract product name
        product_name_locator = product_locator.locator("h3.product_name")
        product_name = product_name_locator.inner_text() if product_name_locator.count() > 0 else "N/A"

        # Get all metal color options and identify the active one
        metal_colors_locators = product_locator.locator(".metal_box").all()  # .all() returns a list of Locators
        active_metal_color = None
        for metal_locator in metal_colors_locators:
            if metal_locator.is_visible() and metal_locator.has_class("active"):  # Ensure visibility and class match
                active_metal_color = metal_locator.inner_text()

        return {
            "price": price,
            "mrp": mrp,
            "product_name": product_name,
            "metal_color": active_metal_color
        }

    def click_product(self, product_index=0):
        """Click on the product (navigate to the product details page)."""
        product_locator = self.page.locator(f"(//div[contains(@class, 'product_box')])[{product_index + 1}]//a")
        product_locator.click()
        time.sleep(2)  # Wait for navigation

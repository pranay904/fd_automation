from playwright.sync_api import Page, expect
import time

class CYOSettingPLPPage:
    def __init__(self, page: Page):
        self.page = page

    def go_to(self):
        """Navigate to the CYO Ring Settings PLP page."""
        self.page.goto("https://payment.ap-diam.com/ring-settings")
        # Ensure the page is fully loaded before interacting with the elements
        self.page.wait_for_selector("(//div[@class='product_box'])[2]", state="visible", timeout=10000)

    def get_product_details(self):
        """Extract details like price, MRP, product name, and active metal color from the second product."""

        # Hardcode the locator to always select the second product
        product_locator = self.page.locator("(//div[@class='product_box'])[2]")  # Selects the second product

        # Wait for the product details container to be visible
        product_locator.wait_for(state="visible", timeout=10000)

        # Extract price within the context of the second product
        price_locator = product_locator.locator("h4.mb-3:visible")  # Ensure it's scoped within the product
        try:
            price_locator.wait_for(state="visible", timeout=10000)  # Wait for price to appear
            price = price_locator.inner_text().strip()
            print(f"Price: {price}")  # Print the price value if successfully located
        except Exception as e:
            price = "Not found"
            print(f"Price not found: {e}")  # Print error if price is not found

        # Extract MRP (if available)
        mrp_locator = product_locator.locator(".plp_mrp_box")
        try:
            mrp_locator.wait_for(state="visible", timeout=10000)
            mrp = mrp_locator.inner_text().strip()
            print(f"MRP: {mrp}")  # Print MRP value if successfully located
        except Exception as e:
            mrp = "Not found"
            print(f"MRP not found: {e}")  # Print error if MRP is not found

        # Extract dynamic product name from <h3 class="grid_view_mob_fs mb-0">
        product_name_locator = product_locator.locator("h3.grid_view_mob_fs.mb-0")
        try:
            product_name_locator.wait_for(state="visible", timeout=10000)
            product_name = product_name_locator.inner_text().strip()
            print(f"Product Name: {product_name}")  # Print the dynamic product name if successfully located
        except Exception as e:
            product_name = "Not found"
            print(f"Product Name not found: {e}")  # Print error if product name is not found

        # Get the currently active metal color
        metal_colors_locator = product_locator.locator(".metal_color .metal_box")
        active_metal_color = None
        try:
            # Look for the div that contains the class 'active' (which represents the selected metal color)
            metal_colors = metal_colors_locator.all()
            for metal_locator in metal_colors:
                if metal_locator.is_visible() and 'active' in metal_locator.get_attribute('class'):
                    active_metal_color = metal_locator.get_attribute('class').split()
                    active_metal_color = [color for color in active_metal_color if color != "metal_box" and color != "active"]
                    active_metal_color = active_metal_color[0] if active_metal_color else None
                    print(f"Active Metal Color: {active_metal_color}")  # Print the active metal color
                    break  # Once we find the active metal color, exit the loop
            if not active_metal_color:
                print("No active metal color found.")
        except Exception as e:
            active_metal_color = "Not found"
            print(f"Error finding metal colors: {e}")

        return {
            "price": price,
            "mrp": mrp,
            "product_name": product_name,
            "metal_color": active_metal_color
        }

    def click_product(self):
        """Click on the second product (navigate to the product details page)."""
        product_locator = self.page.locator("(//div[contains(@class, 'product_box')])[2]//a")  # This is the 2nd product
        product_locator.click()
        time.sleep(2)  # Wait for navigation

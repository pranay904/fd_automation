from playwright.sync_api import Page
import time
import re

class CYOSettingPLPPage:
    def __init__(self, page: Page):
        self.page = page

    def normalize_product_name(self, name: str) -> str:
        """Normalize product name by removing metal prefix and extra spaces."""
        name = name.strip()

        # Remove kt Gold patterns (10kt, 14kt, 18kt etc.)
        name = re.sub(r'^\d+\s*kt\s+(White|Rose|Yellow)\s+Gold\s+', '', name, flags=re.IGNORECASE)

        # Remove Platinum
        name = re.sub(r'^Platinum\s+', '', name, flags=re.IGNORECASE)

        # Clean extra spaces
        name = re.sub(r'\s+', ' ', name)

        return name.strip()

    def go_to(self):
        """Navigate to the CYO Ring Settings PLP page."""
        self.page.goto("https://friendlydiamonds.com/ring-settings")
        self.page.wait_for_selector("(//div[@class='product_box'])[2]", state="visible", timeout=10000)

    def get_product_details(self):
        """Extract details like price, MRP, product name, and active metal color from the second product."""

        product_locator = self.page.locator("(//div[@class='product_box'])[2]")
        product_locator.wait_for(state="visible", timeout=10000)

        # Extract price
        price_locator = product_locator.locator("h4.mb-3:visible")
        try:
            price_locator.wait_for(state="visible", timeout=10000)
            price_text = price_locator.inner_text().strip()
            price_parts = price_text.split()
            price = price_parts[0]
            mrp = price_parts[1] if len(price_parts) > 1 else product_locator.locator(".plp_mrp_box").inner_text().strip()
            print(f"Price: {price}, MRP: {mrp}")
        except Exception as e:
            price, mrp = "Not found", "Not found"
            print(f"Error extracting price/MRP: {e}")

        # ✅ FIXED PRODUCT NAME
        product_name_locator = product_locator.locator("h3.grid_view_mob_fs.mb-0")
        try:
            product_name_locator.wait_for(state="visible", timeout=10000)
            full_name = product_name_locator.inner_text().strip()

            # Apply normalization
            product_name = self.normalize_product_name(full_name)

            print(f"Full Name: {full_name}")
            print(f"Normalized Name: {product_name}")

        except Exception as e:
            product_name = "Not found"
            print(f"Error extracting product name: {e}")

        # Extract active metal color
        active_metal_color = None
        try:
            for metal in product_locator.locator(".metal_color .metal_box").all():
                if 'active' in metal.get_attribute('class'):
                    match = re.search(r'(white|rose|yellow)', metal.get_attribute('class'), re.IGNORECASE)
                    active_metal_color = match.group(0).lower() if match else None
                    break
            print(f"Active Metal Color: {active_metal_color}")
        except Exception as e:
            active_metal_color = "Not found"
            print(f"Error extracting metal color: {e}")

        return {
            "price": price,
            "mrp": mrp,
            "product_name": product_name,
            "metal_color": active_metal_color
        }

    def click_product(self):
        """Click on the second product to go to the details page."""
        product_locator = self.page.locator("(//div[@class='product_box'])[2]//a")
        product_locator.click()
        time.sleep(2)
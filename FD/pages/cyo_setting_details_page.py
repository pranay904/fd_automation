from playwright.sync_api import Page
import time
import re

class CYOSettingDetailsPage:
    def __init__(self, page: Page):
        self.page = page

    def normalize_product_name(self, name: str) -> str:
        """Normalize product name by removing metal prefix and extra spaces."""
        name = name.strip()

        # Remove kt Gold patterns (10kt, 14kt, 18kt etc.)
        name = re.sub(r'^\d+\s*kt\s+(White|Rose|Yellow)\s+Gold\s+', '', name, flags=re.IGNORECASE)

        # Remove Platinum
        name = re.sub(r'^Platinum\s+', '', name, flags=re.IGNORECASE)

        # Clean extra spaces / newlines
        name = re.sub(r'\s+', ' ', name)

        return name.strip()

    def get_product_details(self):
        """Extract product details from the details page and normalize them."""

        # Price
        try:
            price = self.page.locator("h2 span:nth-child(1)").inner_text().strip()
        except:
            price = "Not found"
        print(f"Details Price: {price}")

        # MRP
        try:
            mrp = self.page.locator("h2 span:nth-child(2)").inner_text().strip()
        except:
            mrp = "Not found"
        print(f"Details MRP: {mrp}")

        # FIXED Product Name
        try:
            full_name = self.page.locator(".font-active.mb-3").inner_text().strip()

            product_name = self.normalize_product_name(full_name)

            print(f"Full Name (Details): {full_name}")
            print(f"Normalized Name (Details): {product_name}")

        except Exception as e:
            product_name = "Not found"
            print(f"Error extracting product name: {e}")

        # Metal Color
        try:
            metal_text = self.page.locator("//div[@class='metal_label']//span[@class='me-2']").inner_text().strip()
            match = re.search(r'(white|rose|yellow)', metal_text, re.IGNORECASE)
            metal_color = match.group(0).lower() if match else metal_text.lower()
        except:
            metal_color = "Not found"
        print(f"Details Metal Color: {metal_color}")

        return {
            "price": price,
            "mrp": mrp,
            "product_name": product_name,
            "metal_color": metal_color
        }

    def verify_product_details(self, expected_details: dict):
        """Compare normalized details page values with PLP values."""
        details = self.get_product_details()

        # Optional safety normalization again before compare
        plp_name = expected_details["product_name"].strip().lower()
        details_name = details["product_name"].strip().lower()

        assert details["price"] == expected_details["price"], \
            f"Price mismatch | PLP: {expected_details['price']} | Details: {details['price']}"

        assert details["mrp"] == expected_details["mrp"], \
            f"MRP mismatch | PLP: {expected_details['mrp']} | Details: {details['mrp']}"

        assert plp_name == details_name, \
            f"Product Name mismatch | PLP: {expected_details['product_name']} | Details: {details['product_name']}"

        assert details["metal_color"] == expected_details["metal_color"], \
            f"Metal Color mismatch | PLP: {expected_details['metal_color']} | Details: {details['metal_color']}"

    def select_this_setting(self):
        select_button = self.page.locator("//span[normalize-space()='Select this Setting']")
        select_button.click()
        time.sleep(5)
from playwright.sync_api import Page
import time
import re

class CYOSettingDetailsPage:
    def __init__(self, page: Page):
        self.page = page

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

        # Product Name (remove "14kt White Gold" prefix)
        try:
            full_name = self.page.locator(".font-active.mb-3").inner_text().strip()
            product_name = re.sub(r'^(14kt|18kt|Platinum)\s+(White|Rose|Yellow)\s+Gold\s+', '', full_name, flags=re.IGNORECASE)
        except:
            product_name = "Not found"
        print(f"Details Product Name: {product_name}")

        # Metal Color (normalize to white/rose/yellow)
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

        assert details["price"] == expected_details["price"], f"Price mismatch | PLP: {expected_details['price']} | Details: {details['price']}"
        assert details["mrp"] == expected_details["mrp"], f"MRP mismatch | PLP: {expected_details['mrp']} | Details: {details['mrp']}"
        assert details["product_name"] == expected_details["product_name"], f"Product Name mismatch | PLP: {expected_details['product_name']} | Details: {details['product_name']}"
        assert details["metal_color"] == expected_details["metal_color"], f"Metal Color mismatch | PLP: {expected_details['metal_color']} | Details: {details['metal_color']}"

    def select_this_setting(self):
        select_button = self.page.locator("//span[normalize-space()='Select this Setting']")
        #self.page.scroll_into_view_if_needed(select_button)
        select_button.click()
        time.sleep(5)

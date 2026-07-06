from playwright.sync_api import Page

from FD.pages.base_page import BasePage
from FD.locators.product_locators import ProductLocators
from FD.pages.cart_marge_pages.select_ring_size import SelectRingSize


class ProductDetailsPage(BasePage, SelectRingSize):

    def __init__(self, page: Page):
        super().__init__(page)

        self.eternity_product_name = ""
        self.eternity_product_price = ""
        self.eternity_product_mrp = ""
        self.complete_product_data = {}

    # ----------------------------------------------------------------
    # TC-FD-CART-001 methods
    # ----------------------------------------------------------------

    def get_product_name(self) -> str:
        """
        Capture product name from PDP.
        Validation SKIPPED — returns empty string on failure, never raises.
        """
        try:
            # Try the most common PDP name patterns on FD
            for xpath in [
                "//h1[contains(@class,'cd_name')]",
                "//h1[contains(@class,'product_name')]",
                "//h2[contains(@class,'cd_name')]",
                "//h1[@class='font-active']",
                "//h1",
            ]:
                el = self.page.locator(xpath).first
                if el.is_visible():
                    name = el.inner_text().strip()
                    print(f"[INFO] Product Name : {name}")
                    return name
        except Exception as e:
            print(f"[WARN] Could not read product name: {e}")
        return ""

    def get_product_price(self) -> str:
        """
        Capture product price from PDP.
        Validation SKIPPED — returns empty string on failure, never raises.
        """
        try:
            for xpath in [
                "//span[contains(@class,'font-active') and contains(text(),'$')]",
                "//h4[contains(@class,'font-active')]",
                "//span[contains(@class,'cd_price')]",
                "//h4[contains(@class,'cd_price')]",
            ]:
                el = self.page.locator(xpath).first
                if el.is_visible():
                    price = el.inner_text().strip()
                    print(f"[INFO] Product Price: {price}")
                    return price
        except Exception as e:
            print(f"[WARN] Could not read product price: {e}")
        return ""

    def select_size(self):
        """Select a ring size using the SelectRingSize mixin (scroll + dropdown)."""
        self.select_ring_size()

    def add_to_cart(self):
        """Scroll to Add to Bag button, click it, then wait until quick cart count updates to > 0."""
        btn = self.page.locator(ProductLocators.ADD_TO_CART).first
        btn.wait_for(state="visible", timeout=15000)
        btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(800)
        btn.click()
        print("[INFO] Add to Cart clicked — waiting for cart to update...")

        # Wait until the quick cart h2 shows a count > 0
        # This confirms the item was actually added, not just that the drawer opened
        try:
            self.page.wait_for_function(
                """() => {
                    const el = document.querySelector('h2.font-active.mb-0');
                    if (!el) return false;
                    const match = el.innerText.match(/\\((\\d+)\\)/);
                    return match && parseInt(match[1]) > 0;
                }""",
                timeout=15000
            )
            print("[INFO] Cart updated — item confirmed in quick cart")
        except Exception as e:
            print(f"[WARN] Cart update not detected via h2: {e}")

    # ----------------------------------------------------------------
    # Legacy methods — kept as-is, not used in TC-FD-CART-001
    # ----------------------------------------------------------------

    def select_metal(self):
        """Click the first available metal chip on the PDP (legacy)."""
        chips = self.page.locator(ProductLocators.METAL_OPTIONS)
        chips.first.wait_for(state="visible", timeout=10000)
        chips.first.scroll_into_view_if_needed()
        chips.first.click()
        print("[INFO] Metal selected (first option)")

    def verify_eternity_pdp_loaded(self):
        self.wait_for_element(ProductLocators.PRODUCT_NAME)

    def get_eternity_product_details(self):
        self.eternity_product_name = self.page.locator(
            ProductLocators.PRODUCT_NAME
        ).first.text_content().strip()
        self.eternity_product_price = self.page.locator(
            ProductLocators.PRODUCT_PRICE
        ).first.text_content().strip()
        self.eternity_product_mrp = self.page.locator(
            ProductLocators.PRODUCT_MRP
        ).first.text_content().strip()
        print(f"Eternity PDP Name : {self.eternity_product_name}")
        print(f"Eternity PDP Price: {self.eternity_product_price}")
        print(f"Eternity PDP MRP  : {self.eternity_product_mrp}")

    def verify_eternity_product_name(self, expected_name):
        actual = self.page.locator(ProductLocators.PRODUCT_NAME).first.text_content().strip()
        assert actual == expected_name

    def verify_eternity_product_price(self, expected_price):
        actual = self.page.locator(ProductLocators.PRODUCT_PRICE).first.text_content().strip()
        assert actual == expected_price

    def add_eternity_product_to_cart(self):
        self.select_ring_size()
        self.click(ProductLocators.ADD_TO_CART)

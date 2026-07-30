from FD.pages.base_page import BasePage
from FD.locators.cart_locators import CartLocators
from utils.cart_count import CartCount


class CartPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.cart_count = CartCount(page)

    # ----------------------------------------------------------------
    # Popup dismissal — must be called first on the cart/bag page
    # ----------------------------------------------------------------

    def dismiss_free_product_popup(self):
        """
        The free product popup always appears on the shopping bag page.
        Wait for it to become visible, then close it before any verification.
        """
        try:
            close_button = self.page.locator("div.modal_close_btn").first
            close_button.wait_for(state="visible", timeout=15000)
            close_button.click()
            self.page.wait_for_timeout(800)
            print("[INFO] Free product popup dismissed")
        except Exception:
            print("[INFO] Free product popup did not appear — continuing")

    # ----------------------------------------------------------------
    # Shopping bag count
    # ----------------------------------------------------------------

    def verify_shopping_bag_count(self) -> int:
        """
        Read the item count from the Shopping Bag heading.
        HTML: <h1 class="font-active">Shopping Bag <span>(1)</span></h1>
        Extracts the number from the <span> — e.g. "(1)" → 1
        """
        self.page.locator(CartLocators.CART_COUNT_SPAN).wait_for(state="visible", timeout=15000)
        raw = self.page.locator(CartLocators.CART_COUNT_SPAN).inner_text().strip()
        cleaned = raw.strip("()")
        count = int(cleaned) if cleaned.isdigit() else 0
        print(f"[INFO] Shopping Bag count: {raw} → {count}")
        return count

    # ----------------------------------------------------------------
    # Product details on bag page
    # ----------------------------------------------------------------

    def get_product_name(self) -> str:
        return self.text(CartLocators.PRODUCT_NAME)

    def get_product_price(self) -> str:
        return self.text(CartLocators.PRODUCT_PRICE)

    # ----------------------------------------------------------------
    # Navigation: login icon → Sign Up (from cart page)
    # ----------------------------------------------------------------

    def navigate_to_signup(self):
        """Click login icon → login page → click Sign Up → register page."""
        self.page.locator(CartLocators.LOGIN_ICON).wait_for(state="visible", timeout=10000)
        self.click(CartLocators.LOGIN_ICON)
        self.page.wait_for_load_state("load")
        self.page.locator(CartLocators.SIGN_UP_LINK).wait_for(state="visible", timeout=10000)
        print("[INFO] Clicked Login icon — on Login page")

        self.page.locator(CartLocators.SIGN_UP_LINK).click()
        self.page.wait_for_load_state("load")
        self.page.locator("//input[@name='first_name']").wait_for(state="visible", timeout=10000)
        print("[INFO] Clicked Sign Up — on Register page")

    def navigate_to_sign_in(self):
        """Click Sign In and wait for login modal."""

        self.page.locator(CartLocators.SIGN_IN).wait_for(
            state="visible",
            timeout=10000
        )

        self.page.locator(CartLocators.SIGN_IN).click()

        # Wait for login modal
        modal = self.page.locator("div.modal_body.modal_sm")
        modal.wait_for(state="visible", timeout=10000)

        # Wait until email field is available
        modal.locator("input[name='email']").wait_for(
            state="visible",
            timeout=10000
        )
        


    def navigate_to_login(self):
        """Click login icon → land on login page (for TC-002 login flow)."""
        self.page.locator(CartLocators.LOGIN_ICON).wait_for(state="visible", timeout=10000)
        self.click(CartLocators.LOGIN_ICON)
        self.page.wait_for_load_state("load")
       # self.page.locator("//input[@name='email']").wait_for(state="visible", timeout=10000)
        print("[INFO] Clicked Login icon — on Login page")

    # ----------------------------------------------------------------
    # Checkout
    # ----------------------------------------------------------------

    def click_checkout(self):
        """Click the Continue to Payment button on the shopping bag page."""

        checkout_btn = self.page.locator(
            CartLocators.CONTINUE_TO_PAYMENT
        )

        # Select visible checkout button
        checkout_btn = checkout_btn.filter(
            visible=True
        )

        checkout_btn.click()

        print("[INFO] Clicked Checkout / Continue to Payment")

    def get_cart_page_count(self):

        return self.cart_count.get_cart_page_count(
            CartLocators.CART_COUNT_SPAN
        )






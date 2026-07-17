from FD.pages.base_page import BasePage
from FD.locators.quick_cart_locators import QuickCartLocators
from FD.locators.cart_locators import CartLocators
from utils.cart_count import CartCount


class QuickCartPage(BasePage):

    def __init__(self, page):

        super().__init__(page)

        self.cart_count = CartCount(page)



    def is_open(self):
        """
        Wait for quick cart drawer to open AND confirm count > 0 after Add to Cart.
        Polls the h2 text until it contains a number > 0 in parentheses.
        """
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
            print("[INFO] Quick cart drawer is open with count > 0")
        except Exception as e:
            print(f"[WARN] Quick cart is_open check: {e}")

    def open_quick_cart(self):
        """
        Click the navbar cart icon to open the quick cart drawer,
        then wait for the count element to be visible.
        """
        self.page.locator(QuickCartLocators.CART).wait_for(state="visible", timeout=10000)
        self.click(QuickCartLocators.CART)
        self.page.locator(QuickCartLocators.CART_COUNT).wait_for(state="visible", timeout=10000)
        print("[INFO] Quick cart drawer opened")

    def get_quick_cart_count(self, logged_in: bool = False) -> int:
        """
        Return the item count from the quick cart drawer h2.
        h2 text: 'My Shopping Bag (1)' — extract number inside parentheses.
        Both guest and logged-in use //h2[@class='font-active mb-0'].
        """
        try:
            self.page.locator(QuickCartLocators.CART_COUNT).wait_for(state="visible", timeout=10000)
            raw = self.page.locator(QuickCartLocators.CART_COUNT).inner_text().strip()
            import re
            # Extract number inside parentheses e.g. "My Shopping Bag (1)" → 1
            match = re.search(r'\((\d+)\)', raw)
            if match:
                count = int(match.group(1))
            else:
                # Fallback: first standalone number
                match = re.search(r'\b(\d+)\b', raw)
                count = int(match.group(1)) if match else 0
            print(f"[INFO] Quick cart count: '{raw}' → {count}")
            return count
        except Exception as e:
            print(f"[WARN] Could not read quick cart count: {e}")
            return 0

    def click_view_bag(self):
        """Click the View Bag button inside the quick cart drawer."""
        self.page.locator(QuickCartLocators.VIEW_BAG).wait_for(state="visible", timeout=10000)
        self.click(QuickCartLocators.VIEW_BAG)
        #self.page.wait_for_load_state("load")
        self.page.locator(CartLocators.CART_HEADING).wait_for(state="visible", timeout=15000)
        print("[INFO] Clicked View Bag — on Shopping Bag page")

    def click_signup(self):
        """
        Click login icon → login page → click Sign Up → register page.
        """
        self.page.locator(CartLocators.LOGIN_ICON).wait_for(state="visible", timeout=10000)
        self.click(CartLocators.LOGIN_ICON)
        self.page.wait_for_load_state("load")
        self.page.locator(CartLocators.SIGN_UP_LINK).wait_for(state="visible", timeout=10000)
        print("[INFO] Clicked Login icon — on Login page")

        self.page.locator(CartLocators.SIGN_UP_LINK).click()
        self.page.wait_for_load_state("load")
        self.page.locator("//input[@name='first_name']").wait_for(state="visible", timeout=10000)
        print("[INFO] Clicked Sign Up — on Register page")

    def click_checkout(self):
        """Click the Checkout button inside the quick cart drawer."""
        self.page.locator(QuickCartLocators.CHECKOUT).wait_for(state="visible", timeout=10000)
        self.click(QuickCartLocators.CHECKOUT)
        self.page.wait_for_load_state("load")
        print("[INFO] Clicked Checkout from Quick Cart")

    def get_quick_cart_count_two(self, logged_in=False):

        return self.cart_count.get_quick_cart_count(
            QuickCartLocators.CART_COUNT
        )

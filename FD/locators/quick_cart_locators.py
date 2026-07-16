class QuickCartLocators:

    # Navbar cart icon — click to open quick cart drawer
    CART = "//img[@class='new-navbar-util-cart-img']"

    # Cart count badge on the navbar icon (both guest and logged-in)
    # Shown as a small number badge on top of the cart icon
    CART_BADGE = "//span[contains(@class,'cart_count') or contains(@class,'cart-count') or contains(@class,'badge')]"

    # Cart item count inside the quick cart drawer (guest — shown as text like "1 Item")
    # h2 inside the drawer panel
    CART_COUNT = "(//h2[@class='font-active mb-0'])[1]"

    # Cart count after login — same locator, same element
    CART_COUNT_LOGGED_IN = "(//h2[@class='font-active mb-0'])[1]"

    # View Bag button inside the drawer
    VIEW_BAG = ".button-base.view_bag"

    # Checkout button inside the drawer
    CHECKOUT = ".button-base.checkout"

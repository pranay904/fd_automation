


class HomeLocators:
    # Navbar cart icon image — used to click and open quick cart
    CART = "//img[@class='new-navbar-util-cart-img']"

    # Cart count badge number shown on navbar icon
    # <span class="...">1</span> overlaid on the cart icon
    CART_BADGE = "//span[contains(@class,'cart_item_count') or contains(@class,'cart_count') or contains(@class,'item_count')]"

    QUICK_CART = "(//div[@class='produ_block'])[1]"
    QUICK_CART_COUNT = "(//div[@class='shopping_bag_head'])[1]"
    VIEW_BAG = "(//span[@class='button-base view_bag'])[1]"
    CHECKOUT_BAG = "(//div[@class='checkout_bag'])[1]"

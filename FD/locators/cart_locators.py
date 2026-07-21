class CartLocators:

    # Shopping Bag page heading — full text e.g. "Shopping Bag (1)"
    # <h1 class="font-active">Shopping Bag <span>(1)</span></h1>
    CART_HEADING = "//h1[@class='font-active']"

    # Just the count span inside the heading — e.g. "(1)"
    CART_COUNT_SPAN = "//h1[@class='font-active']/span"

    # Product Details on shopping bag page
    PRODUCT_NAME = "//h4[@class='mb-2']"
    PRODUCT_PRICE = "//h4[@class='mb-0 main_price']"
    METAL = "//p[contains(.,'Metal')]/span"

    # Authentication — navbar
    SIGN_IN = "//span[@class='sign_in_box']"
    LOGIN_ICON = "//a[@href='/login']//img"

    # Sign Up link on the login page
    SIGN_UP_LINK = "//a[normalize-space()='Sign Up']"
    SIGN_IN_LINK = "//a[normalize-space()='Sign in']"

    # Checkout button on shopping bag page
    CONTINUE_TO_PAYMENT = "//button[contains(@class,'btn-p-animation') and .//span[normalize-space()='CONTINUE TO PAYMENT']]"
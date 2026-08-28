class CheckoutLocators:
    PRODUCT_NAME = "css=.summary-product-name"
    PRODUCT_PRICE = "css=.summary-price"
    METAL = "css=.summary-metal"
    SIZE = "css=.summary-size"
    QUANTITY = "css=.summary-qty"

    CONTACT_EMAIL = "//input[@id='contact_email']"

    CONTINUE_TO_ADDRESS = "//button[@type='submit' and .//span[normalize-space()='Continue to address']]"




    SHIPPING_FIRST_NAME = (
        "//input[@name='shipping_first_name']"
    )

    SHIPPING_LAST_NAME = (
        "//input[@name='shipping_last_name']"
    )

    COUNTRY = (
        "//select[@name='country']"
    )

    ADDRESS = (
        "//input[@placeholder='Please enter your address']"
    )

    SHIPPING_CITY = (
        "//input[@name='shipping_city']"
    )

    STATE = (
        "//select[@name='state']"
    )

    SHIPPING_POSTCODE = (
        "//input[@name='shipping_postcode']"
    )

    PHONE = (
        "//input[@id='MazInputPhoneNumber-v-0-0-9-0-0-phone']"
    )

    # ================================================================
    # PAYMENT
    # ================================================================

    PROCEED_TO_PAYMENT = (
        "//button[@type='submit' and contains(@class,'contact_continue_btn')]"
    )

    # IMPORTANT:
    # Replace this with the actual stable locator from your
    # payment section if you have a data-testid.
    PAYMENT_SECTION = (
        "//*[contains(normalize-space(),'Payment')]"
    )
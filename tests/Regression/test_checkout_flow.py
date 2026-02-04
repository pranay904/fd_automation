import pytest
from pages.home_page_ele import Guest  # Importing the Guest class
from pages.cyo_setting_plp_page import CYOSettingPLPPage
from pages.cyo_setting_details_page import CYOSettingDetailsPage
from pages.diamond_plp_page import DiamondPLPPage
from pages.diamond_details_page import DiamondDetailsPage
from pages.cart_page import CartPage
from utils.config import CYO_R_URL, DIAMOND_SETTING_URL

@pytest.fixture(scope="function")
def browser(page):
    """Fixture to be used for browser context"""
    return page  # 'page' is provided by the pytest fixture for browser tests

def test_checkout_flow(browser):
    # Initialize page objects
    guest = Guest(browser)
    cyo_setting_plp_page = CYOSettingPLPPage(browser)
    cyo_setting_details_page = CYOSettingDetailsPage(browser)
    diamond_plp_page = DiamondPLPPage(browser)
    diamond_details_page = DiamondDetailsPage(browser)
    cart_page = CartPage(browser)

    # Step 1: Open the base URL
    guest.open_Base_url()

    # Step 2: Navigate to the CYO Ring Settings page
    cyo_setting_plp_page.go_to()

    # Step 3: Get product details (price, MRP, product name, metal color) for the second product
    product_details = cyo_setting_plp_page.get_product_details()

    # Print the product details (for debugging or verification)
    print(f"Product details: {product_details}")

    # Step 4: Click on the second product to go to the CYO Setting details page
    cyo_setting_plp_page.click_product()

    # Step 5: Verify the product details on the CYO Setting details page
    cyo_setting_details_page.verify_product_details(product_details)

    # Step 6: Select this setting on the CYO Setting details page
    cyo_setting_details_page.select_this_setting()

    # Step 7: Open the Loose Diamonds (Diamond Setting) PLP page
    diamond_plp_page.go_to()

    # Step 8: Get diamond details (price, MRP, title, 4Cs) for the first diamond
    diamond_details = diamond_plp_page.get_diamond_details(diamond_index=0)

    # Print the diamond details (for debugging or verification)
    print(f"Diamond details: {diamond_details}")

    # Step 9: Verify diamond details on the diamond details page
    diamond_details_page.verify_diamond_details(diamond_details)

    # Step 10: Add diamond to the ring
    diamond_details_page.add_diamond_to_ring()

    # Step 11: Verify the total price in the cart
    expected_price = str(float(product_details["price"].replace('$', '').replace(',', '')) + float(diamond_details["price"].replace('$', '').replace(',', '')))
    cart_page.verify_total_price(expected_price)

    # Step 12: Add to bag
    cart_page.add_to_bag()



import time

import pytest

from pages.cart_marge_pages import product_details_page
from pages.cart_marge_pages.cart_page import CartPage
from pages.cart_marge_pages.checkout_page import CheckoutPage
from pages.cart_marge_pages.product_details_page import ProductDetailsPage
from pages.cart_marge_pages.quick_cart import QuickCartPage
from pages.checkout_address_page import CheckoutAddress
from pages.cyo_setting_details_page import CYOSettingDetailsPage
from pages.cyo_setting_plp_page import CYOSettingPLPPage
from pages.cyor_complete_page import CompletePage
from pages.diamond_details_page import DiamondDetailsPage
from pages.diamond_plp_page import DiamondPLPPage
from utils.config import RING_SETTING
from pages.base_page import BasePage

def test_cart_reg_checkout_page(page):

    base_page=  BasePage(page)
    ring_setting_url = RING_SETTING
    setting_listing    = CYOSettingPLPPage(page)
    setting_details   = CYOSettingDetailsPage(page)
    diamond_listing  = DiamondPLPPage(page)
    diamonds_details    = DiamondDetailsPage(page)
    complete_page     = CompletePage(page)
    checkout_page =CheckoutAddress(page)

    cart_page = CartPage(page)
    quick_cart_page = QuickCartPage(page)
    checkout = CheckoutPage(page)

    base_page.open_url(ring_setting_url)
    time.sleep(2)

    setting_listing.click_product()

    setting_details.select_this_setting()

    diamond_listing.click_product()

    diamonds_details.add_diamond_to_ring()

    complete_page.select_ring_size()

    complete_page.add_to_bag()

    quick_cart_page.is_open()

    count_guest = quick_cart_page.get_quick_cart_count_two(logged_in=False)

    assert count_guest == 1, f"[FAIL] quick cart count(guest): expected =1, got {count_guest}"

    print( f"[PASS] Quick cart count (guest) = {count_guest}")




    quick_cart_page.click_view_bag()
    cart_page.dismiss_free_product_popup()

    shopping_bag_count= cart_page.verify_shopping_bag_count()

    assert shopping_bag_count  == 1, f"[FAIL] Shopping Bag Count (guest): expected =1, got {shopping_bag_count}"

    print(f"[PASS] Shopping Bag Count (guest) = {shopping_bag_count}")


    cart_page.click_checkout()


    # enter the details on checkout  and register user
    checkout_page.create_account_and_fill_details()
    checkout_page.click_proceed_to_payment()



    invalid_cart_popup = page.locator("//div[@class='modal_body modal_sm']")
    if invalid_cart_popup.is_visible():
        pytest.fail("[FAIL] Invalid cart identifier error popup is displayed — cart merge failed")

    current_url = page.url.lower()
    page_body = page.locator("body").inner_text().lower()

    # Verify user reached payment section
    assert "payment" in page_body, "[FAIL] Payment section not displayed"

    # Verify common checkout errors are absent
    assert "something went wrong" not in page_body, "[FAIL] Error message displayed"
    assert "page not found" not in page_body, "[FAIL] 404 page displayed"
    assert "invalid cart identifier" not in page_body, "[FAIL] Invalid cart identifier displayed"

    # Verify URL
    assert "/checkout/" in current_url, (
        f"[FAIL] User is not on checkout page. Current URL: {current_url}"
    )

    print(f"[PASS] Checkout loaded successfully — URL: {current_url}")







































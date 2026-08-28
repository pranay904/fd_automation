import pytest

from pages.base_page import BasePage

from pages.cart_marge_pages.cart_page import CartPage
from pages.cart_marge_pages.checkout_page import CheckoutPage
from pages.cart_marge_pages.quick_cart import QuickCartPage

from pages.cyo_setting_details_page import CYOSettingDetailsPage
from pages.cyo_setting_plp_page import CYOSettingPLPPage

from pages.diamond_details_page import DiamondDetailsPage
from pages.diamond_plp_page import DiamondPLPPage

from pages.cyor_complete_page import CompletePage

from utils.config import RING_SETTING


def test_cart_guest_checkout_page(page):

    # ================================================================
    # PAGE OBJECTS
    # ================================================================

    base_page = BasePage(page)

    setting_listing = CYOSettingPLPPage(page)
    setting_details = CYOSettingDetailsPage(page)

    diamond_listing = DiamondPLPPage(page)
    diamonds_details = DiamondDetailsPage(page)

    complete_page = CompletePage(page)

    cart_page = CartPage(page)
    quick_cart_page = QuickCartPage(page)

    checkout = CheckoutPage(page)

    # ================================================================
    # 1. OPEN CYO RING SETTING PAGE
    # ================================================================

    base_page.open_url(RING_SETTING)

    # ================================================================
    # 2. SELECT RING SETTING
    # ================================================================

    setting_listing.click_product()

    setting_details.select_this_setting()

    # ================================================================
    # 3. SELECT DIAMOND
    # ================================================================

    diamond_listing.click_product()

    diamonds_details.add_diamond_to_ring()

    # ================================================================
    # 4. COMPLETE RING CONFIGURATION
    # ================================================================

    complete_page.select_ring_size()

    # ================================================================
    # 5. ADD RING TO BAG
    # ================================================================

    complete_page.add_to_bag()

    # ================================================================
    # 6. VERIFY GUEST QUICK CART COUNT
    # ================================================================

    quick_cart_page.is_open()

    count_guest = (
        quick_cart_page.get_quick_cart_count_two(
            logged_in=False
        )
    )

    assert count_guest == 1, (
        "[FAIL] Quick cart count (guest): "
        f"expected = 1, got {count_guest}"
    )

    print(
        f"[PASS] Quick cart count (guest) = {count_guest}"
    )

    # ================================================================
    # 7. OPEN SHOPPING BAG
    # ================================================================

    quick_cart_page.click_view_bag()

    cart_page.dismiss_free_product_popup()

    # ================================================================
    # 8. VERIFY SHOPPING BAG COUNT
    # ================================================================

    shopping_bag_count = (
        cart_page.verify_shopping_bag_count()
    )

    assert shopping_bag_count == 1, (
        "[FAIL] Shopping Bag Count (guest): "
        f"expected = 1, got {shopping_bag_count}"
    )

    print(
        f"[PASS] Shopping Bag Count (guest) = "
        f"{shopping_bag_count}"
    )

    # ================================================================
    # 9. PROCEED TO CHECKOUT
    # ================================================================

    cart_page.click_checkout()

    # ================================================================
    # 10. ENTER GUEST EMAIL
    # ================================================================

    email_result = checkout.enter_guest_email()

    assert email_result is True, (
        "[FAIL] Guest email could not be entered"
    )

    # ================================================================
    # 11. CONTINUE TO ADDRESS
    # ================================================================

    continue_result = checkout.click_continue_to_address()

    assert continue_result is True, (
        "[FAIL] Could not continue from email "
        "to address section"
    )

    # ================================================================
    # 12. FILL SHIPPING ADDRESS
    # ================================================================

    address_result = checkout.fill_shipping_address()

    assert address_result is True, (
        "[FAIL] Shipping address could not be filled"
    )

    # ================================================================
    # 13. PROCEED TO PAYMENT
    # ================================================================

    payment_result = checkout.click_proceed_to_payment()

    assert payment_result is True, (
        "[FAIL] Could not proceed to payment"
    )

    # ================================================================
    # 14. VERIFY PAYMENT SECTION
    # ================================================================

    payment_section_result = (
        checkout.verify_payment_section()
    )

    assert payment_section_result is True, (
        "[FAIL] Payment section did not load successfully"
    )

    # ================================================================
    # FINAL
    # ================================================================

    print(
        "[PASS] Guest CYO checkout completed successfully"
    )

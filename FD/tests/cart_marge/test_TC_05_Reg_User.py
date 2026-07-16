import time

import pytest

from pages.cart_marge_pages.cart_page import CartPage
from pages.cart_marge_pages.checkout_page import CheckoutPage
from pages.cart_marge_pages.homepage import HomePage
from pages.cart_marge_pages.listing import Listing
from pages.cart_marge_pages.product_details_page import ProductDetailsPage
from pages.cart_marge_pages.quick_cart import QuickCartPage
from pages.login.register_page import RegisterPage



def test_reg_cart_marge(page):


    home     = HomePage(page)
    listing  = Listing(page)
    product  = ProductDetailsPage(page)
    quick    = QuickCartPage(page)
    cart     = CartPage(page)
    checkout = CheckoutPage(page)
    register = RegisterPage(page)



    register.open_register_production()

    register.register_user()

    home.go_to_listing("ETERNITY")

    listing.open_first_product()
    product.select_size()

    product.add_to_cart()

    quick.is_open()
    time.sleep(1)
    count_reg = quick.get_quick_cart_count(logged_in=True)
    assert count_reg == 1, f"[FAIL] Quick cart count (Register_user): expected 1, got {count_reg}"
    print(f"[PASS] Quick cart count (Register_user) = {count_reg}")


    home.go_to_listing("FIVE_STONE")

    listing.open_first_product()
    product.select_size()

    product.add_to_cart()

    quick.is_open()
    time.sleep(1)

    count_reg = quick.get_quick_cart_count(logged_in=True)
    assert count_reg == 2, f"[FAIL] Quick cart count (Register_user): expected 2, got {count_reg}"
    print(f"[PASS] Quick cart count (Register_user) = {count_reg}")

    quick.click_view_bag()
    cart.dismiss_free_product_popup()


    bag_count = cart.verify_shopping_bag_count()
    assert bag_count == 2, (
        f"[FAIL] Shopping Bag count: expected 2, got {bag_count}"
    )
    print(f"[PASS] Shopping Bag count = {bag_count}")

    page.go_back()
    product.select_size()


    product.add_to_cart()

    quick.is_open()
    time.sleep(1)

    count_reg = quick.get_quick_cart_count(logged_in=True)
    assert count_reg == 3, f"[FAIL] Quick cart count (Register_user): expected 3, got {count_reg}"
    print(f"[PASS] Quick cart count (Register_user) = {count_reg}")


    quick.click_checkout()
    cart.dismiss_free_product_popup()

    invalid_cart_popup = page.locator("//div[@class='modal_body modal_sm']")
    if invalid_cart_popup.is_visible():
        pytest.fail("[FAIL] Invalid cart identifier error popup is displayed — cart merge failed")

    current_url = page.url
    page_body   = page.locator("body").inner_text().lower()

    assert "404"                  not in page_body,    "[FAIL] 404 error on checkout page"
    assert "something went wrong" not in page_body,    "[FAIL] Error message on checkout page"
    assert "error"                not in current_url.lower(), (
        f"[FAIL] 'error' found in checkout URL: {current_url}"
    )

    print(f"[PASS] Checkout loaded without errors — URL: {current_url}")























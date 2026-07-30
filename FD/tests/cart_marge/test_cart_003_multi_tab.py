import time

import pytest

from pages.cart_marge_pages.homepage import HomePage
from pages.cart_marge_pages.listing import Listing
from pages.cart_marge_pages.product_details_page import ProductDetailsPage
from pages.cart_marge_pages.quick_cart import QuickCartPage
from pages.cart_marge_pages.cart_page import CartPage


def test_TC_FD_CART_003(shared_page):


    # TAB 1

    tab1 = shared_page

    home1 = HomePage(tab1)
    listing1 = Listing(tab1)
    product1 = ProductDetailsPage(tab1)
    quick1 = QuickCartPage(tab1)
    cart1 = CartPage(tab1)

    # Step 1
    home1.go_to_listing("TWO_STONE")

    # Step 2
    listing1.open_first_product()
    time.sleep(2)

    # Step 3
    product1.select_size()
    time.sleep(2)

    # Step 4
    product1.add_to_cart()

    quick1.is_open()

    # Step 5
    badge_count = quick1.get_quick_cart_count_two()

    assert badge_count == 1, (
        f"Expected cart badge 1 "
        f"But got {badge_count}"
    )

    print("[PASS] Tab1 cart badge = 1")
    time.sleep(2)

    quick1.click_view_bag()

    cart1.dismiss_free_product_popup()

    bag_count = cart1.get_cart_page_count()

    assert bag_count == 1, (
        f"Expected shopping bag count 1 "
        f"But got {bag_count}"
    )

    print("[PASS] Tab1 shopping bag count = 1")

    # TAB 2
    # Same Browser Context = Same Session


    tab2 = tab1.context.new_page()

    home2 = HomePage(tab2)
    listing2 = Listing(tab2)
    product2 = ProductDetailsPage(tab2)
    quick2 = QuickCartPage(tab2)
    cart2 = CartPage(tab2)

    # Step 7
    home2.open_home()

    # Step 8
    tab2.reload()
    tab2.wait_for_load_state("load")

    quick2.open_quick_cart()
    time.sleep(2)

    badge_tab2 = quick2.get_quick_cart_count()

    assert badge_tab2 == 1, (
        f"Cart not synced in Tab2. "
        f"Expected 1 got {badge_tab2}"
    )

    print("[PASS] Tab2 cart synced")

    # Step 9
    quick2.click_view_bag()

    bag_count = cart2.get_cart_page_count()

    assert bag_count == 1

    print("[PASS] Tab2 shopping bag count = 1")

    # -------------------------------------------------------
    # Step 10
    # Add another product from Tab2
    # -------------------------------------------------------

    home2.go_to_listing("FIVE_STONE")

    # Step 11
    listing2.open_first_product()
    time.sleep(2)

    # Step 12
    product2.select_size()
    time.sleep(2)

    # Step 13
    product2.add_to_cart()
    time.sleep(3)

    quick2.is_open()

    # Step 14
    badge_count = quick2.get_quick_cart_count_two()
    time.sleep(1)

    assert badge_count == 2, (
        f"Expected cart badge 2 "
        f"But got {badge_count}"
    )

    print("[PASS] Tab2 cart updated = 2")

    # -------------------------------------------------------
    # Verify Tab1 sync
    # -------------------------------------------------------

    tab1.bring_to_front()
    tab1.go_back()
    tab1.reload()

    quick1.open_quick_cart()

    badge_tab1 = quick1.get_quick_cart_count_two()

    assert badge_tab1 == 2, (
        f"Expected Tab1 badge 2 "
        f"But got {badge_tab1}"
    )

    print("[PASS] Tab1 synced successfully")

    # Switch back to Tab2

    tab2.bring_to_front()
    tab2.wait_for_load_state("load")

    # Optional if your application requires refresh
    # tab2.reload()
    # tab2.wait_for_load_state("load")

    #quick2.open_quick_cart()
    time.sleep(1)

    # Checkout

    quick2.click_checkout()

    invalid_cart_popup = tab2.locator(
        "//div[@class='modal_body modal_sm']"
    )

    if invalid_cart_popup.is_visible():
        pytest.fail(
            "[FAIL] Invalid cart identifier popup is displayed"
        )

    current_url = tab2.url

    page_body = tab2.locator("body").inner_text().lower()

    assert "404" not in page_body, "[FAIL] 404 error on checkout page"

    assert "something went wrong" not in page_body, (
        "[FAIL] Error message on checkout page"
    )

    assert "error" not in current_url.lower(), (
        f"[FAIL] Error found in URL: {current_url}"
    )

    print(f"[PASS] Checkout loaded successfully - {current_url}")
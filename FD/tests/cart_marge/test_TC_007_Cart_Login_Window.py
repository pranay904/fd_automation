import pytest

from pages.cart_marge_pages.cart_page import CartPage
from pages.cart_marge_pages.checkout_page import CheckoutPage
from pages.cart_marge_pages.homepage import HomePage
from pages.cart_marge_pages.listing import Listing
from pages.cart_marge_pages.product_details_page import ProductDetailsPage
from pages.cart_marge_pages.quick_cart import QuickCartPage
from pages.login.login_page import LoginPage
from tests.cart_marge.shared_cart_data import load, update_cart_count


def test_TC_007_Cart_Login_Window(shared_page):
    page = shared_page

    home     = HomePage(page)
    listing  = Listing(page)
    product  = ProductDetailsPage(page)
    quick    = QuickCartPage(page)
    cart     = CartPage(page)
    checkout = CheckoutPage(page)
    login    = LoginPage(page)


    data = load()

    if not data or not data["email"]:
        pytest.skip("Run TC-001 first. No saved user found.")

    email = data["email"]
    password = data["password"]
    saved_cart = data["cart_count"]


    home.open_home()

    # Step 2 — Navigate to Eternity Ring listing page

    home.go_to_listing("ETERNITY")

    # Step 3 — Open first product

    listing.open_first_product()

    product.select_ring_size()
    product.add_to_cart()

    # Step 6 — Quick cart drawer opens; verify count == 1 (guest)
    quick.is_open()

    count_guest = quick.get_quick_cart_count(logged_in=False)
    assert count_guest == 1, f"[FAIL] Quick cart count (guest): expected 1, got {count_guest}"
    print(f"[PASS] Quick cart count (guest) = {count_guest}")

    # ------------------------------------------------------------------
    # Step 9 — Click View Bag → Shopping Bag page
    # ------------------------------------------------------------------
    quick.click_view_bag()
    cart.dismiss_free_product_popup()

    # ------------------------------------------------------------------
    # Step 10 — Verify Shopping Bag count == 1
    # ------------------------------------------------------------------
    bag_count = cart.verify_shopping_bag_count()
    assert bag_count == 1, f"[FAIL] Shopping Bag count: expected 1, got {bag_count}"
    print(f"[PASS] Shopping Bag count = {bag_count}")

    # ------------------------------------------------------------------
    # Step 11 — Login from cart modal
    # ------------------------------------------------------------------
    cart.navigate_to_sign_in()

    login.login_cart_modal(email, password)

    # Wait for login modal to close
    page.locator("div.modal_body.modal_sm").wait_for(
        state="hidden",
        timeout=15000
    )

    # Give the cart merge API time to update the UI
    page.wait_for_timeout(3000)

    # ------------------------------------------------------------------
    # Step 12 — Verify merged cart count
    # ------------------------------------------------------------------
    count_merged = cart.verify_shopping_bag_count()

    expected = saved_cart + count_guest

    print(f"[INFO] Saved cart      : {saved_cart}")
    print(f"[INFO] Guest cart      : {count_guest}")
    print(f"[INFO] Expected merged : {expected}")
    print(f"[INFO] Actual merged   : {count_merged}")

    assert count_merged == expected, (
        f"[FAIL] Cart merge failed. "
        f"Expected {expected}, got {count_merged}"
    )

    print(
        f"[PASS] Cart merged successfully "
        f"({saved_cart} existing + {count_guest} guest = {count_merged})"
    )

    # ------------------------------------------------------------------
    # Step 13 — Checkout → no error
    # ------------------------------------------------------------------
    cart.click_checkout()

    invalid_popup = page.locator("//div[@class='modal_body modal_sm']")

    if invalid_popup.is_visible():
        pytest.fail(
            "[FAIL] Invalid cart identifier popup displayed — cart merge failed"
        )

    current_url = page.url
    page_body = page.locator("body").inner_text().lower()

    assert "404" not in page_body, "[FAIL] 404 on checkout page"
    assert "something went wrong" not in page_body, "[FAIL] Error on checkout page"
    assert "error" not in current_url.lower(), (
        f"[FAIL] Error in URL: {current_url}"
    )

    print(f"[PASS] Checkout loaded without errors — URL: {current_url}")

    # ------------------------------------------------------------------
    # Save latest cart count only after complete TC-007 success
    # ------------------------------------------------------------------
    update_cart_count(count_merged)

    print(f"[INFO] Updated shared cart count in JSON = {count_merged}")


















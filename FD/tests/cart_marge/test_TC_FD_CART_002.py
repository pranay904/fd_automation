"""
TC-FD-CART-002 — Guest User → Login (Existing Account) → Cart Merge Validation
================================================================================

Pre-condition: TC-001 must run first in the same session.
               After TC-001 completes checkout, this test continues in the same browser.

Exact flow:
  1.  Go to home page (continuing from TC-001 checkout page)
  2.  Hover profile icon → click Logout
  3.  Verify cart count == 0 after logout
  4.  Navigate to Eternity Ring listing page
  5.  Open the first product (PDP)
  6.  Capture product name & price (validation SKIPPED)
  7.  Select ring size → click Add to Cart
  8.  Quick cart drawer opens → assert count == 1 (guest)
  9.  Click View Bag → land on Shopping Bag page
  10. Verify Shopping Bag heading count == 1
  11. From cart page click Login icon → login with TC-001 credentials
      (that account already has 1 item in cart from TC-001)
  12. Open quick cart → assert count == 2 (guest 1 + existing user 1)
  13. Click Checkout → assert no error
"""

import pytest

from FD.pages.cart_marge_pages.homepage import HomePage
from FD.pages.cart_marge_pages.listing import Listing
from FD.pages.cart_marge_pages.product_details_page import ProductDetailsPage
from FD.pages.cart_marge_pages.quick_cart import QuickCartPage
from FD.pages.cart_marge_pages.cart_page import CartPage
from FD.pages.cart_marge_pages.checkout_page import CheckoutPage
from FD.pages.login.login_page import LoginPage
from FD.tests.cart_marge.shared_cart_data import load, update_cart_count



def test_TC_FD_CART_002(shared_page):
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

    # Step 1 — Go home (browser is still open from TC-001)

    home.open_home()

    # Step 2 — Navigate to Eternity Ring listing page

    home.go_to_listing("ETERNITY")

    # Step 3 — Open first product

    listing.open_first_product()

    # Step 4 — Capture name & price (validation SKIPPED)
    name  = product.get_product_name()
    price = product.get_product_price()

    # Step 5 — Select ring size → Add to Cart (no metal selection on PDP)

    product.select_size()
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
    # Step 11 — Click Login icon → login with TC-001 credentials
    # ------------------------------------------------------------------
    cart.navigate_to_login()
    login.login_with_credentials(email, password)

    # ------------------------------------------------------------------
    # Step 12 — Open quick cart → assert count == 2
    #            guest cart (1) + user existing cart (1) = 2
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # Step 12 — Open quick cart → verify cart merge
    # ------------------------------------------------------------------

    quick.open_quick_cart()

    count_merged = quick.get_quick_cart_count(logged_in=True)

    expected = saved_cart + count_guest

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
    quick.click_checkout()

    invalid_popup = page.locator("//div[@class='modal_body modal_sm']")
    if invalid_popup.is_visible():
        pytest.fail("[FAIL] Invalid cart identifier popup displayed — cart merge failed")

    current_url = page.url
    page_body   = page.locator("body").inner_text().lower()
    assert "404" not in page_body, "[FAIL] 404 on checkout page"
    assert "something went wrong" not in page_body, "[FAIL] Error on checkout page"
    assert "error" not in current_url.lower(), f"[FAIL] Error in URL: {current_url}"

    print(f"[PASS] Checkout loaded without errors — URL: {current_url}")

    # --------------------------------------------------------------
    # Save latest cart count only after complete TC-002 success
    # --------------------------------------------------------------
    update_cart_count(expected)

    print(
        f"[INFO] Updated shared cart count in JSON = {count_merged}"
    )

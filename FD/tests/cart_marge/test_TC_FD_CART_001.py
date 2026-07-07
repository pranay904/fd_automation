"""
TC-FD-CART-001 — Guest User → Signup → Cart Merge Validation
=============================================================

Exact flow:
  1.  Open the website (home page)
  2.  Navigate to the Eternity Ring listing page
  3.  Open the first product (PDP)
  4.  Capture product name & price  ← validation SKIPPED for now (code kept, assertions commented)
  5.  Select metal + ring size → click Add to Cart
  6.  Quick cart drawer opens → read count from drawer → assert == 1
  7.  Click View Bag from quick cart → land on Shopping Bag page
  8.  Verify Shopping Bag heading count == 1
      HTML: <h1 class="font-active">Shopping Bag <span>(1)</span></h1>
  9.  From cart page click Login icon (//a[@href='/login']//img)
      → on Login page click Sign Up (//a[normalize-space()='Sign Up'])
  10. Complete registration (new user with generated email)
  11. After signup, open quick cart via navbar icon
      → read count from //h2[@class='font-active mb-0']  → assert == 1
      (cart merge: guest cart preserved after signup)
  12. Click Checkout from quick cart drawer → assert no error page
"""

import pytest

from FD.pages.cart_marge_pages.homepage import HomePage
from FD.pages.cart_marge_pages.listing import Listing
from FD.pages.cart_marge_pages.product_details_page import ProductDetailsPage
from FD.pages.cart_marge_pages.quick_cart import QuickCartPage
from FD.pages.cart_marge_pages.cart_page import CartPage
from FD.pages.cart_marge_pages.checkout_page import CheckoutPage
from FD.pages.login.register_page import RegisterPage


def test_TC_FD_CART_001(shared_page):
    page = shared_page

    home     = HomePage(page)
    listing  = Listing(page)
    product  = ProductDetailsPage(page)
    quick    = QuickCartPage(page)
    cart     = CartPage(page)
    checkout = CheckoutPage(page)
    register = RegisterPage(page)

    # ------------------------------------------------------------------
    # Step 1 — Open the website
    # ------------------------------------------------------------------
    home.open_home()

    # ------------------------------------------------------------------
    # Step 2 — Navigate to Eternity Ring listing page
    # ------------------------------------------------------------------
    home.go_to_listing("ETERNITY")

    # ------------------------------------------------------------------
    # Step 3 — Open the first product on the listing
    # ------------------------------------------------------------------
    listing.open_first_product()

    # ------------------------------------------------------------------
    # Step 4 — Capture product name & price
    #           Validation SKIPPED for now — code kept, assertions off
    # ------------------------------------------------------------------
    name  = product.get_product_name()
    price = product.get_product_price()

    # TODO: uncomment when product/price validation is ready
    # assert name  != "", "Product name should not be empty"
    # assert price != "", "Product price should not be empty"

    # ------------------------------------------------------------------
    # Step 5 — Select ring size → Add to Cart (no metal selection on PDP)
    # ------------------------------------------------------------------
    product.select_size()
    product.add_to_cart()

    # ------------------------------------------------------------------
    # Step 6 — Quick cart drawer opens; verify count == 1 (guest)
    # ------------------------------------------------------------------
    quick.is_open()

    quick_count_guest = quick.get_quick_cart_count(logged_in=False)
    assert quick_count_guest == 1, (
        f"[FAIL] Quick cart count after Add to Cart: expected 1, got {quick_count_guest}"
    )
    print(f"[PASS] Quick cart count (guest) = {quick_count_guest}")

    # ------------------------------------------------------------------
    # Step 7 — Click View Bag → navigate to Shopping Bag page
    # ------------------------------------------------------------------
    quick.click_view_bag()

    # Dismiss the free product popup if it appears on the bag page
    cart.dismiss_free_product_popup()

    # ------------------------------------------------------------------
    # Step 8 — Verify Shopping Bag page count == 1
    #           <h1 class="font-active">Shopping Bag <span>(1)</span></h1>
    # ------------------------------------------------------------------
    bag_count = cart.verify_shopping_bag_count()
    assert bag_count == 1, (
        f"[FAIL] Shopping Bag count: expected 1, got {bag_count}"
    )
    print(f"[PASS] Shopping Bag count = {bag_count}")

    # ------------------------------------------------------------------
    # Step 9 — From cart page: click Login icon → click Sign Up
    #           //a[@href='/login']//img  →  //a[normalize-space()='Sign Up']
    # ------------------------------------------------------------------
    cart.navigate_to_signup()

    # ------------------------------------------------------------------
    # Step 10 — Complete registration with a fresh generated email
    # ------------------------------------------------------------------
    register.register_user()

    # Save credentials for TC-002


    # ------------------------------------------------------------------
    # Step 11 — After signup: open quick cart via navbar icon
    #            Check count using //h2[@class='font-active mb-0']
    #            Cart merge: guest cart must be preserved → count == 1
    # ------------------------------------------------------------------
    quick.open_quick_cart()

    quick_count_merged = quick.get_quick_cart_count(logged_in=True)
    assert quick_count_merged == 1, (
        f"[FAIL] Cart merge failed — quick cart count after signup: "
        f"expected 1, got {quick_count_merged}"
    )
    print(f"[PASS] Quick cart count (post-signup / merged) = {quick_count_merged}")

    from FD.tests.cart_marge.shared_cart_data import save

    save(
        email=register.email,
        password=register.email,  # FD password = email
        cart_count=quick_count_merged
    )

    print("[INFO] Registration details saved for TC-002")

    # ------------------------------------------------------------------
    # Step 12 — Click Checkout from quick cart → assert no error
    # ------------------------------------------------------------------
    quick.click_checkout()

    # Check for invalid cart identifier popup — if visible, test fails
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

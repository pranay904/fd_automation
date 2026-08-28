"""
TC-FD-CART-002 — Existing User Login Cart Merge Validation

Test Scenario:
Validate that a guest user's cart is merged with an existing user's cart
after login, while preserving both guest and account cart items.

Pre-condition:
TC-FD-CART-001 must be executed successfully first.
User credentials and existing cart count are stored from TC-FD-CART-001.

Test Steps:
1. Open website home page.
2. Add a new product to cart as a guest user.
3. Verify guest cart contains one item.
4. Navigate to Shopping Bag and verify cart count.
5. Login using the existing account created in TC-FD-CART-001.
6. Verify guest cart and existing user cart are merged successfully.
7. Proceed to checkout and validate no cart or page errors.

Expected Result:
Guest cart items should merge with the existing user's cart after login,
and checkout should load successfully without errors.
"""

import pytest

from FD.pages.cart_marge_pages.homepage import HomePage
from FD.pages.cart_marge_pages.listing import Listing
from FD.pages.cart_marge_pages.product_details_page import ProductDetailsPage
from FD.pages.cart_marge_pages.quick_cart import QuickCartPage
from FD.pages.cart_marge_pages.cart_page import CartPage
from FD.pages.login.login_page import LoginPage
from FD.tests.cart_marge.shared_cart_data import load, update_cart_count


def test_TC_FD_CART_002(shared_page):

    page = shared_page

    home = HomePage(page)
    listing = Listing(page)
    product = ProductDetailsPage(page)
    quick = QuickCartPage(page)
    cart = CartPage(page)
    login = LoginPage(page)

    # Load user details created in TC-001
    data = load()

    if not data or not data.get("email"):
        pytest.skip("TC-001 must be executed first. No saved user credentials found.")

    email = data["email"]
    password = data["password"]
    existing_cart_count = data["cart_count"]

    # Add product to guest cart
    home.open_home()
    home.go_to_listing("ETERNITY")

    listing.open_first_product()

    product.select_size()
    product.add_to_cart()

    # Validate guest cart count
    quick.is_open()

    guest_cart_count = quick.get_quick_cart_count(logged_in=False)

    assert guest_cart_count == 1, (
        f"Guest cart count mismatch. Expected: 1, Actual: {guest_cart_count}"
    )

    # Validate shopping bag count
    quick.click_view_bag()

    cart.dismiss_free_product_popup()

    bag_count = cart.verify_shopping_bag_count()

    assert bag_count == 1, (
        f"Shopping bag count mismatch. Expected: 1, Actual: {bag_count}"
    )

    # Login with existing user account
    cart.navigate_to_login()

    login.login_with_credentials(email, password)

    # Validate cart merge after login
    quick.open_quick_cart()

    merged_cart_count = quick.get_quick_cart_count(logged_in=True)

    expected_cart_count = existing_cart_count + guest_cart_count

    assert merged_cart_count == expected_cart_count, (
        f"Cart merge failed. Expected: {expected_cart_count}, "
        f"Actual: {merged_cart_count}"
    )

    # Proceed to checkout
    quick.click_checkout()

    invalid_popup = page.locator("//div[@class='modal_body modal_sm']")

    if invalid_popup.is_visible():
        pytest.fail("Invalid cart identifier popup displayed after cart merge")

    current_url = page.url
    page_text = page.locator("body").inner_text().lower()

    assert "404" not in page_text, "404 error displayed on checkout page"
    assert "something went wrong" not in page_text, (
        "Checkout page displayed an error message"
    )
    assert "error" not in current_url.lower(), (
        f"Checkout redirected to error URL: {current_url}"
    )

    # Update shared cart data after successful validation
    update_cart_count(merged_cart_count)
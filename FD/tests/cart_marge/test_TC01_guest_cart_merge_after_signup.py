"""
TC-FD-CART-001 — Guest User Signup and Cart Merge Validation

Test Scenario:
Validate that a guest user's cart items are preserved after account registration
and successfully merged into the registered user's cart.

Test Steps:
1. Open the website home page.
2. Navigate to the Eternity Ring listing page.
3. Open the first product details page.
4. Select ring size and add the product to cart.
5. Verify guest quick cart contains one item.
6. Navigate to Shopping Bag and verify cart item count.
7. Navigate to Login and create a new user account.
8. Verify guest cart is retained after signup.
9. Proceed to checkout and verify no cart or page errors are displayed.

Expected Result:
Guest cart should merge successfully with the newly registered account,
maintaining the cart item count and allowing checkout navigation.
"""

import pytest

from FD.pages.cart_marge_pages.homepage import HomePage
from FD.pages.cart_marge_pages.listing import Listing
from FD.pages.cart_marge_pages.product_details_page import ProductDetailsPage
from FD.pages.cart_marge_pages.quick_cart import QuickCartPage
from FD.pages.cart_marge_pages.cart_page import CartPage
from FD.pages.login.register_page import RegisterPage


def test_TC_FD_CART_001(shared_page):
    page = shared_page

    home = HomePage(page)
    listing = Listing(page)
    product = ProductDetailsPage(page)
    quick = QuickCartPage(page)
    cart = CartPage(page)
    register = RegisterPage(page)

    # Open website and navigate to product listing
    home.open_home()
    home.go_to_listing("ETERNITY")

    # Open first product and add item to cart
    listing.open_first_product()
    product.select_size()
    product.add_to_cart()

    # Validate guest quick cart count
    quick.is_open()

    guest_cart_count = quick.get_quick_cart_count(logged_in=False)

    assert guest_cart_count == 1, (
        f"Guest cart count mismatch. Expected: 1, Actual: {guest_cart_count}"
    )

    # Navigate to shopping bag and validate item count
    quick.click_view_bag()

    cart.dismiss_free_product_popup()

    bag_count = cart.verify_shopping_bag_count()

    assert bag_count == 1, (
        f"Shopping bag count mismatch. Expected: 1, Actual: {bag_count}"
    )

    # Register new user account
    cart.navigate_to_signup()

    register.register_user()

    # Validate guest cart merge after signup
    quick.open_quick_cart()

    merged_cart_count = quick.get_quick_cart_count(logged_in=True)

    assert merged_cart_count == 1, (
        f"Cart merge failed. Expected: 1, Actual: {merged_cart_count}"
    )

    # Store user details for dependent test cases
    from FD.tests.cart_marge.shared_cart_data import save

    save(
        email=register.email,
        password=register.email,
        cart_count=merged_cart_count
    )

    # Proceed to checkout and validate page availability
    quick.click_checkout()

    invalid_cart_popup = page.locator("//div[@class='modal_body modal_sm']")

    if invalid_cart_popup.is_visible():
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
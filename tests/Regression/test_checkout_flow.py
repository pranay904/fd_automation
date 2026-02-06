import time
import pytest
from pages.cyo_setting_plp_page import CYOSettingPLPPage
from pages.cyo_setting_details_page import CYOSettingDetailsPage
from pages.diamond_plp_page import DiamondPLPPage
from pages.diamond_details_page import DiamondDetailsPage
from pages.cyor_complete_page import CompletePage  # Import the CompletePage


@pytest.fixture(scope="function")
def browser(page):
    """
    Fixture for providing the page object to the test.
    """
    return page


@pytest.fixture(scope="function")
def cyo_pages(browser):
    """
    Fixture to initialize Setting and Diamond pages.
    """
    return {
        "setting_plp": CYOSettingPLPPage(browser),
        "setting_details": CYOSettingDetailsPage(browser),
        "diamond_plp": DiamondPLPPage(browser),
        "diamond_details": DiamondDetailsPage(browser),
        "complete": CompletePage(browser)  # Adding the CompletePage to the fixture
    }


def test_setting_and_diamond_details_match(cyo_pages):
    """
    Test to verify setting details + diamond details match between PLP and details pages.
    """

    setting_plp = cyo_pages["setting_plp"]
    setting_details = cyo_pages["setting_details"]
    diamond_plp = cyo_pages["diamond_plp"]
    diamond_details = cyo_pages["diamond_details"]
    complete = cyo_pages["complete"]  # Accessing the Complete page

    # -------------------- SETTING PLP --------------------
    setting_plp.go_to()
    plp_setting_details = setting_plp.get_product_details()

    # Click on setting
    setting_plp.click_product()

    # Verify setting details page
    try:
        setting_details.verify_product_details(plp_setting_details)
        print("Setting details match between PLP and Details page.")
    except AssertionError as e:
        print(f"Setting validation failed: {e}")
        raise

    # Select setting
    setting_details.select_this_setting()

    # -------------------- DIAMOND PLP --------------------
    plp_diamond_details = diamond_plp.get_diamond_details()

    # Click on diamond to go to details page
    diamond_plp.click_product()

    # -------------------- DIAMOND DETAILS --------------------
    try:
        diamond_details.verify_diamond_details(plp_diamond_details)
        print("Diamond details match between PLP and Details page.")
    except AssertionError as e:
        print(f"Diamond validation failed: {e}")
        raise

    # -------------------- COMPLETE PAGE --------------------
    # After adding diamond to the ring, we verify the Complete page
    diamond_details.add_diamond_to_ring()

    time.sleep(6)  # Wait for the Complete page to load

    # Perform validation for Complete page
    validate_complete_page(complete, plp_setting_details, plp_diamond_details)


def validate_complete_page(complete, plp_setting_details, plp_diamond_details):
    """
    Validate all details on the Complete page.
    """
    # Verify Stepper
    try:
        complete.verify_stepper(plp_setting_details, plp_diamond_details)
        print("Stepper verification PASSED.")
    except AssertionError as e:
        print(f"Stepper verification failed: {e}")
        raise

    # Verify Heading and Total Price
    try:
        total_price, total_mrp = complete.verify_heading_and_total_price(
            plp_setting_details, plp_diamond_details
        )
        print(f"Total price: {total_price}, Total MRP: {total_mrp}")
    except AssertionError as e:
        print(f"Heading and Total Price verification failed: {e}")
        raise

    # Verify Saved Amount
    try:
        complete.verify_saved_amount(total_price, total_mrp)
        print("Saved amount verification PASSED.")
    except AssertionError as e:
        print(f"Saved amount verification failed: {e}")
        raise

    # Verify Setting Summary
    try:
        complete.verify_setting_summary(plp_setting_details)
        print("Setting summary verification PASSED.")
    except AssertionError as e:
        print(f"Setting summary verification failed: {e}")
        raise

    # Verify Diamond Summary
    try:
        complete.verify_diamond_summary(plp_diamond_details)
        print("Diamond summary verification PASSED.")
    except AssertionError as e:
        print(f"Diamond summary verification failed: {e}")
        raise

    # Verify Ring Size Selection
    try:
        ring_size = complete.select_ring_size()
        print(f"Ring size selected: {ring_size}")
    except AssertionError as e:
        print(f"Ring size verification failed: {e}")
        raise

    # Verify Shipment Date
    try:
        shipment = complete.get_estimated_shipment()
        print(f"Estimated shipment date: {shipment}")
    except AssertionError as e:
        print(f"Shipment date verification failed: {e}")
        raise

    # Optionally, Add to Bag
    try:
        complete.add_to_bag()
        print("Diamond added to bag successfully.")
    except AssertionError as e:
        print(f"Add to Bag verification failed: {e}")
        raise

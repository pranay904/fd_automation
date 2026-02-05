#
#
# import pytest
# from pages.cyo_setting_details_page import CYOSettingDetailsPage
# from pages.cyo_setting_plp_page import CYOSettingPLPPage
#
# @pytest.fixture(scope="function")
# def browser(page):
#     """
#     Fixture for providing the page object to the test.
#     """
#     return page
#
# @pytest.fixture(scope="function")
# def cyo_pages(browser):
#     """
#     Fixture to initialize the pages for the CYO settings (PLP and Details page).
#     """
#     plp_page = CYOSettingPLPPage(browser)
#     details_page = CYOSettingDetailsPage(browser)
#     return {
#         "plp_page": plp_page,
#         "details_page": details_page
#     }
#
# def test_product_details_match(cyo_pages):
#     """
#     Test to verify that product details from PLP match the details page.
#     """
#     plp_page = cyo_pages["plp_page"]
#     details_page = cyo_pages["details_page"]
#
#     # Navigate to the PLP page and extract product details
#     plp_page.go_to()
#     plp_product_details = plp_page.get_product_details()
#
#     # Click on the product to go to the details page
#     plp_page.click_product()
#
#     # Get product details from the details page
#     details_product_details = details_page.get_product_details()
#
#
#     # Verify that the details from both pages match
#     try:
#         details_page.verify_product_details(plp_product_details)
#         print("Test Passed: Product details match between PLP and Details page.")
#     except AssertionError as e:
#         print(f"Test Failed: {e}")
#         raise
#
# def test_select_product_setting(cyo_pages):
#     """
#     Test to verify that the product setting can be selected correctly.
#     """
#     plp_page = cyo_pages["plp_page"]
#     details_page = cyo_pages["details_page"]
#
#     # Navigate to the PLP page and click the product
#     #plp_page.go_to()
#     #plp_page.click_product()
#
#     # Select the product setting from the details page
#     details_page.select_this_setting()
#
#     # Add assertions or checks to confirm the product setting selection
#     # assert page.url == "expected_url_after_selection"  # Replace with actual expected URL or condition
#     # print("Test Passed: Successfully selected the product setting.")
import time

import pytest
from pages.cyo_setting_plp_page import CYOSettingPLPPage
from pages.cyo_setting_details_page import CYOSettingDetailsPage
from pages.diamond_plp_page import DiamondPLPPage
from pages.diamond_details_page import DiamondDetailsPage


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
        "diamond_details": DiamondDetailsPage(browser)
    }


def test_setting_and_diamond_details_match(cyo_pages):
    """
    Test to verify setting details + diamond details match between PLP and details pages.
    """

    setting_plp = cyo_pages["setting_plp"]
    setting_details = cyo_pages["setting_details"]
    diamond_plp = cyo_pages["diamond_plp"]
    diamond_details = cyo_pages["diamond_details"]

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


def test_add_diamond_to_ring(cyo_pages):
    """
    Test to verify diamond can be added to ring after selecting setting.
    """

    diamond_details = cyo_pages["diamond_details"]

    # Add diamond to ring
    diamond_details.add_diamond_to_ring()
    time.sleep(6)

    # Add assertions or validations if required
    # assert page.url == "expected_url_after_add"
    # print("Test Passed: Diamond added to ring successfully.")






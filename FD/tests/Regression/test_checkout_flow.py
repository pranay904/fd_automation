"""
test_checkout_flow.py
---------------------
Full checkout flow test updated with NEW ShoppingBag class
"""

import pytest

from FD.pages.cyo_setting_plp_page import CYOSettingPLPPage
from FD.pages.cyo_setting_details_page import CYOSettingDetailsPage
from FD.pages.diamond_plp_page import DiamondPLPPage
from FD.pages.diamond_details_page import DiamondDetailsPage
from FD.pages.cyor_complete_page import CompletePage
from FD.pages.cart_page import CartPage
from FD.pages.payment_page import PaymentPage
from FD.pages.shopping_page import ShoppingBag

from FD.utils.retry import retry_on_failure


@pytest.fixture(scope="function")
def browser(page):
    return page


@pytest.fixture(scope="function")
def pages(browser):
    return {
        "setting_plp":     CYOSettingPLPPage(browser),
        "setting_details": CYOSettingDetailsPage(browser),
        "diamond_plp":     DiamondPLPPage(browser),
        "diamond_details": DiamondDetailsPage(browser),
        "complete":        CompletePage(browser),
        "cart":            CartPage(browser),
        "shopping_bag":    ShoppingBag(browser),
    }


def test_setting_and_diamond_details_match(pages):

    setting_plp     = pages["setting_plp"]
    setting_details = pages["setting_details"]
    diamond_plp     = pages["diamond_plp"]
    diamond_details = pages["diamond_details"]
    complete        = pages["complete"]
    cart            = pages["cart"]
    shopping_bag    = pages["shopping_bag"]

    all_results = []

    # ============================================================
    # STEP 1 : SETTING PLP
    # ============================================================

    print("\n========== STEP 1: SETTING PLP ==========")

    retry_on_failure(setting_plp.page, lambda: setting_plp.go_to())

    plp_setting_details = setting_plp.get_product_details()

    setting_plp.click_product()

    # ============================================================
    # STEP 2 : SETTING DETAILS PAGE
    # ============================================================

    print("\n========== STEP 2: SETTING DETAILS PAGE ==========")

    setting_match_result = verify_setting_details(
        setting_details,
        plp_setting_details
    )

    all_results.append(setting_match_result)

    setting_details.select_this_setting()

    # ============================================================
    # STEP 3 : DIAMOND PLP
    # ============================================================

    print("\n========== STEP 3: DIAMOND PLP ==========")

    plp_diamond_details = diamond_plp.get_diamond_details()

    diamond_plp.click_product()

    # ============================================================
    # STEP 4 : DIAMOND DETAILS PAGE
    # ============================================================

    print("\n========== STEP 4: DIAMOND DETAILS PAGE ==========")

    diamond_match_result = verify_diamond_details(
        diamond_details,
        plp_diamond_details
    )

    all_results.append(diamond_match_result)

    # ============================================================
    # STEP 5 : COMPLETE PAGE
    # ============================================================

    print("\n========== STEP 5: COMPLETE PAGE ==========")

    diamond_details.add_diamond_to_ring()

    complete.page.locator(
        "div.price_box h2"
    ).wait_for(state="visible", timeout=15000)

    complete.page.locator(
        "div.prod_list_box"
    ).first.wait_for(state="visible", timeout=15000)

    complete_results, complete_data = verify_complete_page(
        complete,
        plp_setting_details,
        plp_diamond_details
    )

    all_results.extend(complete_results)

    # ============================================================
    # STEP 6 : QUICK CART
    # ============================================================

    print("\n========== STEP 6: QUICK CART ==========")

    cart_results = cart.verify_quick_cart(
        setting_details=plp_setting_details,
        diamond_details=plp_diamond_details
    )

    all_results.extend(cart_results)

    # ============================================================
    # STEP 7 : SHOPPING BAG PAGE
    # ============================================================

    print("\n========== STEP 7: SHOPPING BAG PAGE ==========")

    # ---------------------------------------------------
    # DISMISS FREE PRODUCT POPUP
    # ---------------------------------------------------

    popup_result = shopping_bag.dismiss_free_product_popup()

    all_results.append(popup_result)

    # ---------- SETTING SUMMARY ----------

    all_results.extend(
        shopping_bag.verify_setting_summary(
            plp_setting_details
        )
    )

    # ---------- DIAMOND SUMMARY ----------

    all_results.extend(
        shopping_bag.verify_diamond_summary(
            plp_diamond_details
        )
    )

    # ---------- RING SIZE ----------

    all_results.append(
        shopping_bag.verify_ring_size_in_bag(
            complete_data.get("ring_size", "")
        )
    )

    # ---------- SHIPMENT DATE ----------

    all_results.append(
        shopping_bag.verify_shipment_date_in_bag(
            complete_data.get("shipment_date", "")
        )
    )

    # ---------- SUMMARY PRICE ----------

    all_results.extend(
        shopping_bag.verify_summary_prices(
            complete_data.get("total_price", ""),
            complete_data.get("total_mrp", "")
        )
    )

    # ============================================================
    # STEP 8 : CONTINUE TO PAYMENT
    # ============================================================

    print("\n========== STEP 8: CONTINUE TO PAYMENT ==========")

    continue_result = shopping_bag.click_continue_to_payment()

    all_results.append(continue_result)

    # ============================================================
    # STEP 9 : CHECKOUT ADDRESS PAGE
    # ============================================================

    print("\n========== STEP 9: CHECKOUT ADDRESS PAGE ==========")

    from FD.pages.checkout_address_page import CheckoutAddress

    checkout_address = CheckoutAddress(shopping_bag.page)

    # ---------- VERIFY PAGE ----------

    all_results.append(
        checkout_address.verify_title()
    )

    # ---------- DISMISS POPUP ----------

    all_results.append(
        checkout_address.dismiss_modal()
    )

    # ---------- FILL ADDRESS ----------

    all_results.append(
        checkout_address.create_account_and_fill_details()
    )

    # ---------- PROCEED TO PAYMENT ----------
    # ---------- PROCEED TO PAYMENT ----------

    all_results.append(
        checkout_address.click_proceed_to_payment()
    )

    # ============================================================
    # STEP 10 : PAYMENT PAGE

    print("\n========== STEP 10: PAYMENT PAGE ==========")


    payment_page = PaymentPage(
        shopping_bag.page
    )

    # ------------------------------------------------------------
    # VERIFY PAYMENT PAGE TITLE
    # ------------------------------------------------------------

    print("\n========== VERIFY PAYMENT PAGE TITLE ==========")

    payment_title_result = (
        payment_page.verify_title()
    )

    all_results.append(
        payment_title_result
    )

    # ------------------------------------------------------------
    # VERIFY BANK WIRE PRICE
    # ------------------------------------------------------------

    print("\n========== VERIFY BANK WIRE PRICE ==========")

    payment_price_result = (
        payment_page.verify_bank_wire_price(
            complete_data.get("total_price", "")
        )
    )

    all_results.append(
        payment_price_result
    )

    # ============================================================
    # FINAL SUMMARY
    # ============================================================

    print_summary(all_results)

    # ============================================================
    # FINAL SUMMARY
    # ============================================================

    print_summary(all_results)

    failed_steps = [
        result for result in all_results
        if result["status"] == "FAIL"
    ]

    if failed_steps:

        failed_names = [
            result["step"]
            for result in failed_steps
        ]

        pytest.fail(
            f"{len(failed_steps)} step(s) failed: {failed_names}",
            pytrace=False
        )


# ===================================================================
# HELPER METHODS
# ===================================================================

def verify_setting_details(setting_details_page, plp_setting_details):

    step_name = "Setting Details - PLP vs Details Page Match"

    try:

        setting_details_page.verify_product_details(
            plp_setting_details
        )

        print("  [PASS] Setting details match")

        return {
            "step": step_name,
            "expected": str(plp_setting_details),
            "actual": "Details page matches PLP",
            "status": "PASS",
            "error": ""
        }

    except AssertionError as assertion_error:

        print(f"  [FAIL] {assertion_error}")

        return {
            "step": step_name,
            "expected": str(plp_setting_details),
            "actual": "Mismatch found",
            "status": "FAIL",
            "error": str(assertion_error)
        }

    except Exception as unexpected_error:

        print(f"  [FAIL] {unexpected_error}")

        return {
            "step": step_name,
            "expected": str(plp_setting_details),
            "actual": "Error occurred",
            "status": "FAIL",
            "error": str(unexpected_error)
        }


def verify_diamond_details(diamond_details_page, plp_diamond_details):

    step_name = "Diamond Details - PLP vs Details Page Match"

    try:

        diamond_details_page.verify_diamond_details(
            plp_diamond_details
        )

        print("  [PASS] Diamond details match")

        return {
            "step": step_name,
            "expected": str(plp_diamond_details),
            "actual": "Details page matches PLP",
            "status": "PASS",
            "error": ""
        }

    except AssertionError as assertion_error:

        print(f"  [FAIL] {assertion_error}")

        return {
            "step": step_name,
            "expected": str(plp_diamond_details),
            "actual": "Mismatch found",
            "status": "FAIL",
            "error": str(assertion_error)
        }

    except Exception as unexpected_error:

        print(f"  [FAIL] {unexpected_error}")

        return {
            "step": step_name,
            "expected": str(plp_diamond_details),
            "actual": "Error occurred",
            "status": "FAIL",
            "error": str(unexpected_error)
        }


def verify_complete_page(
        complete_page,
        plp_setting_details,
        plp_diamond_details
):

    results = []

    data = {
        "ring_size": "",
        "total_price": "",
        "total_mrp": "",
        "shipment_date": "",
    }

    print("\n========== COMPLETE PAGE VERIFICATIONS ==========")

    # ---------------------------------------------------
    # STEP : TOTAL PRICE
    # ---------------------------------------------------

    total_price = "N/A"
    total_mrp = "N/A"

    try:

        total_price, total_mrp = (
            complete_page.verify_heading_and_total_price(
                plp_setting_details,
                plp_diamond_details
            )
        )

        data["total_price"] = total_price
        data["total_mrp"] = total_mrp

        results.append({
            "step": "Complete Page - Total Price and MRP",
            "expected": "Price and MRP match",
            "actual": f"{total_price} | {total_mrp}",
            "status": "PASS",
            "error": ""
        })

        print("  [PASS] Total Price")

    except Exception as error:

        results.append({
            "step": "Complete Page - Total Price and MRP",
            "expected": "Price and MRP match",
            "actual": "Check failed",
            "status": "FAIL",
            "error": str(error)
        })

    # ---------------------------------------------------
    # STEP : RING SIZE
    # ---------------------------------------------------

    try:

        selected_ring_size = complete_page.select_ring_size()

        data["ring_size"] = selected_ring_size

        results.append({
            "step": "Complete Page - Ring Size",
            "expected": "Ring size selected",
            "actual": selected_ring_size,
            "status": "PASS",
            "error": ""
        })

        print(f"  [PASS] Ring Size: {selected_ring_size}")

    except Exception as error:

        results.append({
            "step": "Complete Page - Ring Size",
            "expected": "Ring size selected",
            "actual": "Selection failed",
            "status": "FAIL",
            "error": str(error)
        })

    # ---------------------------------------------------
    # STEP : SHIPMENT DATE
    # ---------------------------------------------------

    try:

        shipment_date = complete_page.get_estimated_shipment()

        data["shipment_date"] = shipment_date

        results.append({
            "step": "Complete Page - Shipment Date",
            "expected": "Shipment date visible",
            "actual": shipment_date,
            "status": "PASS",
            "error": ""
        })

        print(f"  [PASS] Shipment Date: {shipment_date}")

    except Exception as error:

        results.append({
            "step": "Complete Page - Shipment Date",
            "expected": "Shipment date visible",
            "actual": "Not found",
            "status": "FAIL",
            "error": str(error)
        })

    # ---------------------------------------------------
    # STEP : ADD TO BAG
    # ---------------------------------------------------

    try:

        complete_page.add_to_bag()

        results.append({
            "step": "Complete Page - Add To Bag",
            "expected": "Button clicked",
            "actual": "Quick cart opened",
            "status": "PASS",
            "error": ""
        })

        print("  [PASS] Add To Bag")

    except Exception as error:

        results.append({
            "step": "Complete Page - Add To Bag",
            "expected": "Button clicked",
            "actual": "Click failed",
            "status": "FAIL",
            "error": str(error)
        })

    return results, data




def print_summary(all_results):

    total_steps = len(all_results)

    passed_count = sum(
        1 for result in all_results
        if result["status"] == "PASS"
    )

    failed_count = sum(
        1 for result in all_results
        if result["status"] == "FAIL"
    )

    skipped_count = sum(
        1 for result in all_results
        if result["status"] == "SKIP"
    )

    print(f"\n{'=' * 60}")
    print("CHECKOUT FLOW TEST SUMMARY")
    print(f"TOTAL   : {total_steps}")
    print(f"PASSED  : {passed_count}")
    print(f"FAILED  : {failed_count}")
    print(f"SKIPPED : {skipped_count}")
    print(f"{'=' * 60}")

    if failed_count > 0:

        print("\nFAILED STEPS:\n")

        for result in all_results:

            if result["status"] == "FAIL":

                print(f"STEP     : {result['step']}")
                print(f"EXPECTED : {result['expected']}")
                print(f"ACTUAL   : {result['actual']}")
                print(f"ERROR    : {result['error']}")
                print()













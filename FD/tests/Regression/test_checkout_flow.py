import pytest
from FD.pages.cyo_setting_plp_page import CYOSettingPLPPage
from FD.pages.cyo_setting_details_page import CYOSettingDetailsPage
from FD.pages.diamond_plp_page import DiamondPLPPage
from FD.pages.diamond_details_page import DiamondDetailsPage
from FD.pages.cyor_complete_page import CompletePage
from FD.pages.cart_page import CartPage
from FD.utils.retry import retry_on_failure
from FD.utils.logger import logger


@pytest.fixture(scope="function")
def browser(page):
    return page


@pytest.fixture(scope="function")
def cyo_pages(browser):
    return {
        "setting_plp":     CYOSettingPLPPage(browser),
        "setting_details": CYOSettingDetailsPage(browser),
        "diamond_plp":     DiamondPLPPage(browser),
        "diamond_details": DiamondDetailsPage(browser),
        "complete":        CompletePage(browser),
        "cart":            CartPage(browser),
    }


def test_setting_and_diamond_details_match(cyo_pages):
    setting_plp     = cyo_pages["setting_plp"]
    setting_details = cyo_pages["setting_details"]
    diamond_plp     = cyo_pages["diamond_plp"]
    diamond_details = cyo_pages["diamond_details"]
    complete        = cyo_pages["complete"]
    cart            = cyo_pages["cart"]

    all_validations = []

    # -------------------- SETTING PLP --------------------
    logger.info("Step: Setting PLP")
    retry_on_failure(setting_plp.page, lambda: setting_plp.go_to())
    plp_setting_details = setting_plp.get_product_details()
    setting_plp.click_product()

    # -------------------- SETTING DETAILS --------------------
    logger.info("Step: Setting Details")
    try:
        setting_details.verify_product_details(plp_setting_details)
        all_validations.append({
            "step": "Setting Details Match (PLP vs Details)",
            "expected": str(plp_setting_details),
            "actual": "Matched",
            "status": "PASS",
            "error": ""
        })
        print("  [PASS] Setting details match between PLP and Details page.")
    except AssertionError as e:
        all_validations.append({
            "step": "Setting Details Match (PLP vs Details)",
            "expected": str(plp_setting_details),
            "actual": "Mismatch",
            "status": "FAIL",
            "error": str(e)
        })
        print(f"  [FAIL] Setting details mismatch: {e}")

    setting_details.select_this_setting()

    # -------------------- DIAMOND PLP --------------------
    logger.info("Step: Diamond PLP")
    plp_diamond_details = diamond_plp.get_diamond_details()
    diamond_plp.click_product()

    # -------------------- DIAMOND DETAILS --------------------
    logger.info("Step: Diamond Details")
    try:
        diamond_details.verify_diamond_details(plp_diamond_details)
        all_validations.append({
            "step": "Diamond Details Match (PLP vs Details)",
            "expected": str(plp_diamond_details),
            "actual": "Matched",
            "status": "PASS",
            "error": ""
        })
        print("  [PASS] Diamond details match between PLP and Details page.")
    except AssertionError as e:
        all_validations.append({
            "step": "Diamond Details Match (PLP vs Details)",
            "expected": str(plp_diamond_details),
            "actual": "Mismatch",
            "status": "FAIL",
            "error": str(e)
        })
        print(f"  [FAIL] Diamond details mismatch: {e}")

    # -------------------- COMPLETE PAGE --------------------
    logger.info("Step: Complete Page")
    diamond_details.add_diamond_to_ring()

    complete.page.locator("div.price_box h2").wait_for(state="visible", timeout=15000)
    complete.page.locator("div.prod_list_box").first.wait_for(state="visible", timeout=15000)

    complete_validations = _validate_complete_page(complete, plp_setting_details, plp_diamond_details)
    all_validations.extend(complete_validations)

    # -------------------- CART VALIDATION --------------------
    logger.info("Step: Cart Validation")
    cart_validations = _validate_cart(cart, plp_setting_details, plp_diamond_details)
    all_validations.extend(cart_validations)

    # -------------------- SUMMARY --------------------
    _print_summary(all_validations)

    failed = [v for v in all_validations if v["status"] == "FAIL"]
    if failed:
        pytest.fail(
            f"{len(failed)} step(s) failed: {[v['step'] for v in failed]}",
            pytrace=False
        )


def _validate_complete_page(complete, plp_setting_details, plp_diamond_details):
    """Run complete page validations, return list of result dicts."""
    validations = []
    print("\n=========== COMPLETE PAGE VALIDATION ===========")

    # Stepper
    try:
        complete.verify_stepper(plp_setting_details, plp_diamond_details)
        validations.append({"step": "Complete - Stepper", "expected": "Stepper correct",
                            "actual": "Passed", "status": "PASS", "error": ""})
        print("  [PASS] Stepper")
    except Exception as e:
        validations.append({"step": "Complete - Stepper", "expected": "Stepper correct",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Stepper: {e}")

    # Total price
    try:
        total_price, total_mrp = complete.verify_heading_and_total_price(
            plp_setting_details, plp_diamond_details
        )
        validations.append({"step": "Complete - Total Price & MRP", "expected": "Prices match",
                            "actual": f"Price={total_price} MRP={total_mrp}", "status": "PASS", "error": ""})
        print(f"  [PASS] Total Price={total_price} MRP={total_mrp}")
    except Exception as e:
        total_price, total_mrp = "N/A", "N/A"
        validations.append({"step": "Complete - Total Price & MRP", "expected": "Prices match",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Total Price: {e}")

    # Saved amount
    try:
        complete.verify_saved_amount(total_price, total_mrp)
        validations.append({"step": "Complete - Saved Amount", "expected": "Saved amount correct",
                            "actual": "Passed", "status": "PASS", "error": ""})
        print("  [PASS] Saved Amount")
    except Exception as e:
        validations.append({"step": "Complete - Saved Amount", "expected": "Saved amount correct",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Saved Amount: {e}")

    # Setting summary
    try:
        complete.verify_setting_summary(plp_setting_details)
        validations.append({"step": "Complete - Setting Summary", "expected": "Setting summary correct",
                            "actual": "Passed", "status": "PASS", "error": ""})
        print("  [PASS] Setting Summary")
    except Exception as e:
        validations.append({"step": "Complete - Setting Summary", "expected": "Setting summary correct",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Setting Summary: {e}")

    # Diamond summary
    try:
        complete.verify_diamond_summary(plp_diamond_details)
        validations.append({"step": "Complete - Diamond Summary", "expected": "Diamond summary correct",
                            "actual": "Passed", "status": "PASS", "error": ""})
        print("  [PASS] Diamond Summary")
    except Exception as e:
        validations.append({"step": "Complete - Diamond Summary", "expected": "Diamond summary correct",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Diamond Summary: {e}")

    # Ring size
    try:
        ring_size = complete.select_ring_size()
        validations.append({"step": "Complete - Ring Size Selection", "expected": "Ring size selected",
                            "actual": ring_size, "status": "PASS", "error": ""})
        print(f"  [PASS] Ring Size: {ring_size}")
    except Exception as e:
        validations.append({"step": "Complete - Ring Size Selection", "expected": "Ring size selected",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Ring Size: {e}")

    # Shipment date
    try:
        shipment = complete.get_estimated_shipment()
        validations.append({"step": "Complete - Estimated Shipment", "expected": "Shipment date present",
                            "actual": shipment, "status": "PASS", "error": ""})
        print(f"  [PASS] Shipment: {shipment}")
    except Exception as e:
        validations.append({"step": "Complete - Estimated Shipment", "expected": "Shipment date present",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Shipment: {e}")

    # Add to bag
    try:
        complete.add_to_bag()
        validations.append({"step": "Complete - Add to Bag", "expected": "Add to Bag clicked",
                            "actual": "Success", "status": "PASS", "error": ""})
        print("  [PASS] Add to Bag")
    except Exception as e:
        validations.append({"step": "Complete - Add to Bag", "expected": "Add to Bag clicked",
                            "actual": "Failed", "status": "FAIL", "error": str(e)})
        print(f"  [FAIL] Add to Bag: {e}")

    return validations


def _validate_cart(cart, plp_setting_details, plp_diamond_details):
    """Validate quick cart after Add to Bag — cart opens automatically."""
    print("\n=========== CART VALIDATION ===========")
    overall, validations = cart.verify_quick_cart(
        setting_details=plp_setting_details,
        diamond_details=plp_diamond_details
    )
    return validations


def _print_summary(validations):
    total   = len(validations)
    passed  = sum(1 for v in validations if v["status"] == "PASS")
    failed  = sum(1 for v in validations if v["status"] == "FAIL")
    skipped = sum(1 for v in validations if v["status"] == "SKIP")

    print(f"\n{'='*55}")
    print(f"  CHECKOUT FLOW SUMMARY")
    print(f"  Total: {total} | PASS: {passed} | FAIL: {failed} | SKIP: {skipped}")
    print(f"{'='*55}")
    if failed:
        print("  FAILED STEPS:")
        for v in validations:
            if v["status"] == "FAIL":
                print(f"    - {v['step']}: {v['error']}")

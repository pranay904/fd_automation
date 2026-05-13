from FD.pages.base_page import BasePage
from FD.pages.cart_page import log_pass, log_fail

import re


class PaymentPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

    # ==========================================================
    # VERIFY PAYMENT PAGE TITLE
    # ==========================================================

    def verify_title(self):

        step_name = "Payment - Page Title"

        try:

            heading = self.page.locator(
                "//h1[contains(text(),'Payment')]"
            )

            heading.wait_for(
                state="visible",
                timeout=15000
            )

            full_text = heading.inner_text().strip()

            print("\n===== PAYMENT PAGE TITLE =====")
            print(f"ACTUAL TITLE : {full_text}")

            if "payment" in full_text.lower():

                print("  [PASS] Payment title verified")

                return log_pass(
                    step_name,
                    "Payment visible",
                    full_text
                )

            else:

                print("  [FAIL] Payment title missing")

                return log_fail(
                    step_name,
                    "Payment visible",
                    full_text,
                    "Title does not contain Payment"
                )

        except Exception as error:

            print(f"  [FAIL] {error}")

            return log_fail(
                step_name,
                "Payment visible",
                "Payment not found",
                str(error)
            )

    # ==========================================================
    # VERIFY BANK WIRE PRICE
    # ==========================================================

    def verify_bank_wire_price(self, total_price):

        step_name = "Payment Page - Bank Wire Price Verification"

        try:

            print("\n===== PAYMENT PAGE PRICE VERIFICATION =====")

            # ==========================================================
            # STEP 1 : GET SUBTOTAL
            # ==========================================================

            subtotal_locator = self.page.locator(
                "//span[contains(text(),'Sub-total')]/following-sibling::span"
            )

            subtotal_locator.wait_for(state="visible")

            subtotal_text = subtotal_locator.inner_text().strip()

            print(f"RAW SUBTOTAL TEXT : {subtotal_text}")

            subtotal_matches = re.findall(
                r"\$[\d,]+\.?\d*",
                subtotal_text
            )

            if not subtotal_matches:
                return log_fail(
                    step_name,
                    "Subtotal visible",
                    subtotal_text,
                    "Subtotal price not found"
                )

            actual_subtotal = float(
                subtotal_matches[0]
                .replace("$", "")
                .replace(",", "")
            )

            expected_subtotal = float(
                total_price
                .replace("$", "")
                .replace(",", "")
            )

            print(f"EXPECTED SUBTOTAL : {expected_subtotal}")
            print(f"ACTUAL SUBTOTAL   : {actual_subtotal}")

            if actual_subtotal == expected_subtotal:

                print("  [PASS] Subtotal matched")

            else:

                print("  [FAIL] Subtotal mismatch")

                return log_fail(
                    step_name,
                    f"${expected_subtotal}",
                    f"${actual_subtotal}",
                    "Subtotal mismatch"
                )

            # ==========================================================
            # STEP 2 : CLICK BANK WIRE
            # ==========================================================

            bank_wire = self.page.get_by_text(
                "Bank Wire",
                exact=True
            )

            bank_wire.wait_for(state="visible")

            bank_wire.click()

            print("  [INFO] Bank wire selected")

            self.page.wait_for_timeout(3000)

            # ==========================================================
            # STEP 3 : APPLY 2% BANK WIRE DISCOUNT
            # ==========================================================

            bank_wire_discount = round(
                actual_subtotal * 0.02,
                2
            )

            after_discount_total = round(
                actual_subtotal - bank_wire_discount,
                2
            )

            print(f"2% DISCOUNT AMOUNT      : {bank_wire_discount}")
            print(f"AFTER BANK WIRE DISCOUNT: {after_discount_total}")

            # ==========================================================
            # STEP 4 : GET TAX %
            # ==========================================================

            tax_percent = 0.0

            tax_locator = self.page.locator(
                "//span[contains(text(),'Tax')]/span"
            )

            if tax_locator.count() > 0:

                tax_text = tax_locator.first.inner_text().strip()

                print(f"TAX TEXT : {tax_text}")

                tax_match = re.search(
                    r"([\d.]+)",
                    tax_text
                )

                if tax_match:
                    tax_percent = float(
                        tax_match.group(1)
                    )

            print(f"TAX % : {tax_percent}")

            # ==========================================================
            # STEP 5 : APPLY TAX
            # ==========================================================

            tax_amount = round(
                after_discount_total * (tax_percent / 100),
                2
            )

            final_expected_total = round(
                after_discount_total + tax_amount,
                2
            )

            print(f"TAX AMOUNT           : {tax_amount}")
            print(f"FINAL EXPECTED TOTAL : {final_expected_total}")

            # ==========================================================
            # STEP 6 : GET FINAL TOTAL
            # ==========================================================

            final_total_locator = self.page.locator(
                "//h3[contains(@class,'font-active flex-custom mb-0') and not(contains(@class,'stick_h3'))]"
            ).last

            final_total_locator.wait_for(
                state="visible",
                timeout=15000
            )

            final_total_text = (
                final_total_locator.inner_text().strip()
            )

            print(f"FINAL TOTAL TEXT : {final_total_text}")

            final_matches = re.findall(
                r"\$[\d,]+\.?\d*",
                final_total_text
            )

            if not final_matches:
                return log_fail(
                    step_name,
                    "Final total visible",
                    final_total_text,
                    "Final amount not found"
                )

            actual_final_total = float(
                final_matches[0]
                .replace("$", "")
                .replace(",", "")
            )

            print(f"ACTUAL FINAL TOTAL : {actual_final_total}")

            # ==========================================================
            # STEP 7 : VERIFY FINAL TOTAL
            # ==========================================================

            if actual_final_total == final_expected_total:

                print("  [PASS] Final amount matched")

                # ==========================================================
                # STEP 8 : CLICK PAY NOW
                # ==========================================================

                pay_now_btn = self.page.get_by_role(
                    "button",
                    name="PAY NOW"
                ).first

                pay_now_btn.wait_for(
                    state="visible",
                    timeout=10000
                )

                pay_now_btn.click()

                print("  [INFO] PAY NOW button clicked")

                return log_pass(
                    step_name,
                    f"${final_expected_total}",
                    f"${actual_final_total}"
                )

            else:

                print("  [FAIL] Final amount mismatch")

                return log_fail(
                    step_name,
                    f"${final_expected_total}",
                    f"${actual_final_total}",
                    "Final amount mismatch"
                )

        except Exception as error:

            print(f"  [FAIL] {error}")

            return log_fail(
                step_name,
                "Bank wire discounted total",
                "Verification failed",
                str(error)
            )
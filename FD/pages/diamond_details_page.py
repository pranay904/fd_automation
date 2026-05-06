import time
from FD.pages.base_page import BasePage
from FD.utils.cyo_normalizer import CYONormalizer


class DiamondDetailsPage(BasePage):

    def verify_diamond_details(self, expected_details: dict):

        # ---------- PRICE ----------
        price_text = self.page.locator("div.price_box.mt-4 h2").inner_text().strip()
        parts = price_text.split()

        price = parts[0]
        mrp = parts[1] if len(parts) > 1 else "Not found"

        # ---------- TITLE DEBUG ----------
        raw_expected_title = expected_details["title"]   # PLP
        raw_actual_title = self.page.locator(".font-active.mb-3").inner_text().strip()  # PDP

        expected_title = CYONormalizer.normalize_text(raw_expected_title)
        actual_title = CYONormalizer.normalize_text(raw_actual_title)

        print("\n===== TITLE DEBUG =====")
        print("PLP Title (Expected) :", raw_expected_title)
        print("PDP Title (Actual)   :", raw_actual_title)
        print("PLP Normalized       :", expected_title)
        print("PDP Normalized       :", actual_title)

        # ---------- SMART TITLE MATCH ----------
        actual_title_data = CYONormalizer.parse_diamond_title(actual_title)
        expected_title_data = CYONormalizer.parse_diamond_title(expected_title)

        print("Parsed Expected:", expected_title_data)
        print("Parsed Actual  :", actual_title_data)

        title_matched = (
            actual_title_data["carat"] == expected_title_data["carat"]
            and actual_title_data["shape"] == expected_title_data["shape"]
        )

        # ---------- 4Cs ----------
        four_cs_text = self.page.locator(
            "div.diam_detail.mb-3 p:nth-child(1)"
        ).inner_text().strip()

        actual_4cs = CYONormalizer.parse_4cs(four_cs_text)
        expected_4cs = CYONormalizer.parse_4cs(expected_details["four_cs"])

        # ---------- MATCH ----------
        price_matched = expected_details["price"] == price
        mrp_matched = expected_details["mrp"] == mrp

        color_matched = actual_4cs["color"].upper() == expected_4cs["color"].upper()
        clarity_matched = actual_4cs["clarity"].upper() == expected_4cs["clarity"].upper()

        cut_matched = (
            CYONormalizer.normalize_cut(actual_4cs["cut"])
            == CYONormalizer.normalize_cut(expected_4cs["cut"])
        )

        print(f"\nPrice: {'MATCHED' if price_matched else 'MISMATCHED'}")
        print(f"MRP: {'MATCHED' if mrp_matched else 'MISMATCHED'}")

        if title_matched:
            print("Title: MATCHED")
        else:
            print("Title: MISMATCHED")

        print(f"Color: {'MATCHED' if color_matched else 'MISMATCHED'}")
        print(f"Clarity: {'MATCHED' if clarity_matched else 'MISMATCHED'}")
        print(f"Cut: {'MATCHED' if cut_matched else 'MISMATCHED'}")

        return all([
            price_matched,
            mrp_matched,
            title_matched,
            color_matched,
            clarity_matched,
            cut_matched
        ])

    def add_diamond_to_ring(self):
        btn = self.page.locator("//span[normalize-space()='add diamond to ring']")
        btn.wait_for(state="visible", timeout=10000)
        btn.scroll_into_view_if_needed()
        btn.click()
        time.sleep(10)
import time
from FD.utils.cyo_normalizer import CYONormalizer


class DiamondPLPPage:
    def __init__(self, page):
        self.page = page

    def get_diamond_details(self):

        diamond_locator = self.page.locator(
            "(//div[@class='diam_block col-lg-3 col-md-4 col-6'])[2]"
        )
        diamond_locator.wait_for(state="visible", timeout=10000)

        # TITLE
        raw_title = diamond_locator.locator(".diam_details .title").inner_text().strip()
        title = CYONormalizer.normalize_text(raw_title)

        # 4Cs
        four_cs = diamond_locator.locator(".four_cs").inner_text().strip()

        # PRICE
        price_text = diamond_locator.locator("h4.mb-0").inner_text().strip()
        parts = price_text.split()

        price = parts[0] if len(parts) > 0 else "Not found"
        mrp = parts[1] if len(parts) > 1 else "Not found"

        print("\n===== PLP DIAMOND =====")
        print("Title :", raw_title)
        print("Price :", price, "MRP:", mrp)
        print("4Cs   :", four_cs)

        return {
            "title": raw_title,
            "four_cs": four_cs,
            "price": price,
            "mrp": mrp
        }

    def click_product(self):
        self.page.locator(
            "(//div[@class='diam_block col-lg-3 col-md-4 col-6'])[2]"
        ).click()
        time.sleep(2)
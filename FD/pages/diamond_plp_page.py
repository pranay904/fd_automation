import time

class DiamondPLPPage:
    def __init__(self, page):
        self.page = page

    def get_diamond_details(self):
        # Wait for the main diamond block
        diamond_locator = self.page.locator(
            "(//div[@class='diam_block col-lg-3 col-md-4 col-6'])[2]"
        )
        diamond_locator.wait_for(state="visible", timeout=10000)
        print("Diamond block is visible.")

        # Title
        title_locator = diamond_locator.locator(".diam_details .title")
        title_locator.wait_for(state="visible", timeout=10000)
        title = title_locator.inner_text().strip()
        print("Diamond_Title_PLP:", title)

        # 4Cs
        four_cs_locator = diamond_locator.locator(".four_cs")
        four_cs_locator.wait_for(state="visible", timeout=10000)
        four_cs = four_cs_locator.inner_text().strip()
        print("diam4Cs:", four_cs)

        # Price & MRP
        price_locator = diamond_locator.locator("h4.mb-0")
        price_locator.wait_for(state="visible", timeout=10000)
        price_text = price_locator.inner_text().strip()
        print("Diamonds Price text PLP:", price_text)

        parts = price_text.split()
        price = parts[0] if len(parts) > 0 else "Not found"
        mrp = parts[1] if len(parts) > 1 else "Not found"
        print("Diamond_Price PLP:", price)
        print("Diamonds_MRP PLP:", mrp)

        return {
            "title": title,
            "four_cs": four_cs,
            "price": price,
            "mrp": mrp
        }

    def click_product(self):
        product_locator = self.page.locator(
            "(//div[@class='diam_block col-lg-3 col-md-4 col-6'])[2]"
        )
        product_locator.click()
        time.sleep(2)

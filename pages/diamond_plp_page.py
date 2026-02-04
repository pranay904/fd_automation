# pages/diamond_plp_page.py
class DiamondPLPPage:
    def __init__(self, page):
        self.page = page

    def go_to(self):
        """Navigate to the Diamonds PLP page."""
        self.page.goto("https://payment.ap-diam.com/loose-diamonds?cyo=ring")

    def get_diamond_details(self, diamond_index=0):
        """Get details for the selected diamond."""
        diamond_locator = self.page.locator(f"(//div[contains(@class, 'diam_block')])[{diamond_index + 1}]")

        # Get title (diamond description)
        title = diamond_locator.locator(".diam_details .title").inner_text()

        # Get the 4Cs (color, clarity, cut, certification)
        four_cs = diamond_locator.locator(".four_cs").inner_text()

        # Get price and MRP (h4)
        price = diamond_locator.locator("h4").inner_text()
        mrp = diamond_locator.locator("h4 .plp_mrp_box").inner_text()

        return {
            "title": title,
            "four_cs": four_cs,
            "price": price,
            "mrp": mrp
        }

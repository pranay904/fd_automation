from pages.base_page import BasePage


class DiamondDetailsPage(BasePage):

    def verify_diamond_details(self, expected_details: dict):
        """Verify the price, carat, and title of the diamond on the diamond details page."""

        # Verify price and MRP
        actual_price = self.page.locator("//span[@class='diamond-price']").inner_text().strip()
        actual_mrp = self.page.locator(
            "//span[@class='diamond-mrp']").inner_text().strip()  # Assuming class for MRP is `diamond-mrp`

        # Verify carat
        actual_carat = self.page.locator(
            "//span[contains(text(),'Carat')]/following-sibling::span").inner_text().strip()

        # Verify title (the name of the diamond)
        actual_title = self.page.locator(
            "//h1[contains(@class,'diamond-title')]").inner_text().strip()  # Assuming class for title is `diamond-title`

        # Verify 4Cs (color, clarity, cut)
        four_cs_locator = self.page.locator(
            "//div[contains(@class,'diamond-fourcs')]").inner_text().strip()  # Assuming there's a div for the 4Cs
        color, clarity, cut = four_cs_locator.split("|")

        # Asserting expected details match actual details
        assert expected_details[
                   "price"] == actual_price, f"Price mismatch: Expected {expected_details['price']}, Found {actual_price}"
        assert expected_details[
                   "mrp"] == actual_mrp, f"MRP mismatch: Expected {expected_details['mrp']}, Found {actual_mrp}"
        assert expected_details[
                   "carat"] == actual_carat, f"Carat mismatch: Expected {expected_details['carat']}, Found {actual_carat}"
        assert expected_details[
                   "title"] == actual_title, f"Title mismatch: Expected {expected_details['title']}, Found {actual_title}"
        assert expected_details[
                   "color"] == color.strip(), f"Color mismatch: Expected {expected_details['color']}, Found {color.strip()}"
        assert expected_details[
                   "clarity"] == clarity.strip(), f"Clarity mismatch: Expected {expected_details['clarity']}, Found {clarity.strip()}"
        assert expected_details[
                   "cut"] == cut.strip(), f"Cut mismatch: Expected {expected_details['cut']}, Found {cut.strip()}"

    def add_diamond_to_ring(self):
        """Click on the 'Add Diamond to Ring' button."""
        add_button = self.page.locator("//button[contains(text(),'Add Diamond to Ring')]")
        self.scroll_into_view(add_button)
        add_button.click()

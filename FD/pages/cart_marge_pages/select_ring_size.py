

class SelectRingSize:

    def __init__(self, page):
        self.page = page

    def select_ring_size(self):

        print("\n===== SELECTING RING SIZE =====")

        # Scroll to the ring size dropdown trigger
        dropdown = self.page.locator("(//div[contains(@class,'current_active')])[1]")
        dropdown.wait_for(state="visible", timeout=10000)
        dropdown.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Click to open the dropdown list
        dropdown.click()
        self.page.wait_for_timeout(800)

        # The ul.p-0 list — wait for it to have visible li items
        dropdown_list = self.page.locator("(//div[contains(@class,'drop_block')])[1]//ul[contains(@class,'p-0')]")
        dropdown_list.wait_for(state="visible", timeout=10000)

        # Select the first li (index 0 = size "3")
        options = dropdown_list.locator("li")
        first_option = options.first
        first_option.wait_for(state="visible", timeout=5000)
        first_option.scroll_into_view_if_needed()

        value = first_option.locator("span").inner_text().strip()
        first_option.click()
        self.page.wait_for_timeout(500)

        print(f"SELECTED RING SIZE: {value}")
        self.complete_product_data["selected_ring_size"] = value

        return value



class SelectRingSize:

    def __init__(self, page):
        self.page = page

    def select_ring_size(self):

        print("\n===== SELECTING RING SIZE =====")

        # Scroll to the ring size dropdown trigger
        dropdown = self.page.locator("(//div[contains(@class,'current_active')])[1]")

        dropdown.wait_for(state="attached", timeout=10000)
        dropdown.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        # Initialize variable
        dropdown_list = None

        # Retry opening the dropdown
        for attempt in range(3):
            try:
                dropdown.scroll_into_view_if_needed()
                self.page.wait_for_timeout(300)

                dropdown.click(timeout=5000)

                candidate = self.page.locator(
                    "(//div[contains(@class,'drop_block')])[1]//ul[contains(@class,'p-0')]"
                )

                candidate.wait_for(state="visible", timeout=3000)

                dropdown_list = candidate
                break

            except Exception as e:
                print(f"Retry {attempt + 1}: Dropdown did not open.")
                print(f"Reason: {e}")

                self.page.mouse.wheel(0, -300)
                self.page.wait_for_timeout(500)

        # If dropdown never opened
        if dropdown_list is None:
            raise Exception("Failed to open Ring Size dropdown after 3 attempts.")

        # Select first option
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

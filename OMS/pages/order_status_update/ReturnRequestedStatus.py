import time
from playwright.sync_api import expect

class ReturnRequestedStatus:
    def __init__(self, page):
        self.page = page
        # Locator for the specific Order Status dropdown
        self.dropdown_locator = "//label[normalize-space()='Select']/ancestor::div[@role='combobox']"

    def select(self):
        # Open the dropdown
        self.page.locator(self.dropdown_locator).click()
        time.sleep(0.5)

        # Get all options from the dropdown
        options = self.page.locator("//div[@role='option']")
        options_count = options.count()
        print(f"Found {options_count} options.")

        # Iterate through all options and select 'Return Requested' if it exists
        for i in range(options_count):
            option_text = options.nth(i).inner_text().strip()  # Get the text and strip any leading/trailing spaces
            print(f"Option {i + 1}: {option_text}")
            if option_text == "Return Requested":
                options.nth(i).click()  # Click the 'Return Requested' option
                print("Selected 'Return Requested'")
                break  # Stop after selecting 'Return Requested'
        else:
            print("'Return Requested' option not found")

        time.sleep(0.5)

        # Click Update button after selection using :text-is
        try:
            update_button = self.page.get_by_role("button", name="Update")
            self.username_input.wait_for(state="visible", timeout=10000)
            update_button.click()
            print("Clicked on the UPDATE button")
        except Exception as e:
            print(f"Error clicking Update button: {e}")

        time.sleep(1)

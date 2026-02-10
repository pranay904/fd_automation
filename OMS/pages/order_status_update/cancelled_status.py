import time
from playwright.sync_api import expect

class CancelledStatus:
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

        # Iterate through all options and select 'Cancelled' if it exists
        for i in range(options_count):
            option_text = options.nth(i).inner_text().strip()  # Get the text and strip any leading/trailing spaces
            print(f"Option {i + 1}: {option_text}")
            if option_text == "Cancelled":
                options.nth(i).click()  # Click the 'Cancelled' option
                print("Selected 'Cancelled'")
                break  # Stop after selecting 'Cancelled'
        else:
            print("'Cancelled' option not found")

        time.sleep(0.5)

        # Click Update button after selection using :text-is
        try:
            update_button = self.page.locator("div.v-card:has-text('Update Order')").get_by_role("button",
                                                                                                 name="Update")

            expect(update_button).to_be_visible()
            update_button.click()
            self.page.wait_for_timeout(2000)
            # dialog = dialog_info.value
            # print("Dialog text:", dialog.message)
            # dialog.accept()

            print("Clicked on UPDATE and accepted confirmation")

        except Exception as e:
            print(f"Error clicking Update button: {e}")


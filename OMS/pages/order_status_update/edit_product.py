import time

from OMS.pages.order_status_update.orderstatusbase import OrderStatusBase


class EditProduct(OrderStatusBase):

    def __init__(self, page):
        super().__init__(page)

    def open_all_order_line(self):
        self.open_order_and_all_order_line()
        self.wait_delay()

    def edit_product_form(self):
        section = self.page.locator(
            "//div[@class='v-row main_row']//div[@class='v-col v-col-8']"
        )
        section.wait_for(state="visible")
        self.hover_with_effect(section)

        edit_product = self.page.get_by_text("Edit Product", exact=True)
        self.click_with_effect(edit_product)

    # --- Fun 1: Update Ring Size ---
    def update_size(self):
        size = "7.25"
        size_options = ["7.25", "7.5", "7.75", "8", "8.25", "8.5",
                        "8.75", "9", "9.25", "9.5", "9.75"]

        size_text = self.page.locator("(//div[@class='v-field__field'])[24]")
        current_size_text = size_text.inner_text().strip()
        print("Selecting size:", current_size_text)

        size_dropdown = self.page.locator("(//div[@role='combobox'])[10]")
        size_dropdown.wait_for(state="visible")
        self.click_with_effect(size_dropdown)

        if current_size_text == size:
            next_size = size_options[(size_options.index(size) + 1) % len(size_options)]
            size_option = self.page.locator(f"//div[@role='option' and normalize-space()='{next_size}']")
        else:
            size_option = self.page.locator(f"//div[@role='option' and normalize-space()='{size}']")

        size_option.wait_for(state="visible")
        self.click_with_effect(size_option)

    # --- Fun 2: Handle Size Change Modal ---
    def handle_size_modal(self):
        accept_modal = self.page.locator("//body/div[@class='v-overlay-container']/div[2]/div[2]/div[1]")

        try:
            accept_modal.wait_for(state="visible", timeout=5000)
            print("Ring size confirmation modal appeared")

            self.hover_with_effect(accept_modal)
            time.sleep(1.5)

            accept_button = accept_modal.locator("(//span[normalize-space()='Continue'])[1]")
            accept_button.wait_for(state="visible")
            self.click_with_effect(accept_button)
            print("Continue button clicked")

            accept_modal.wait_for(state="detached", timeout=10000)
            print("Confirmation modal closed")
            time.sleep(1.5)

        except:
            print("Confirmation modal did not appear")
            time.sleep(2)

    # --- Fun 3: Update Mount ---
    def update_mount(self):
        mount = "Plain"
        mount_options = ["Studded", "Semi Mounting", "Mounting", "Plain"]

        mount_text = self.page.locator("(//div[@class='v-field__field'])[25]")
        current_mount_text = mount_text.inner_text().strip()
        print("Selecting mount:", current_mount_text)

        mount_status_dropdown = self.page.locator("(//div[@role='combobox'])[11]")
        mount_status_dropdown.wait_for(state="visible")
        self.click_with_effect(mount_status_dropdown)

        if current_mount_text == mount:
            next_mount = mount_options[(mount_options.index(mount) + 1) % len(mount_options)]
            mount_option = self.page.locator(f"//div[@role='option' and normalize-space()='{next_mount}']")
        else:
            mount_option = self.page.locator(f"//div[@role='option' and normalize-space()='{mount}']")

        mount_option.wait_for(state="visible")
        self.click_with_effect(mount_option)

    # --- Fun 4: Update Product Details ---
    def update_product_details(self):
        # Update Inscription
        inscription = self.page.get_by_label("Add Inscription")
        inscription.click()
        self.fill_with_effect(inscription, "Test QA Automation")

        # Update Certificate Number
        certificate = self.page.get_by_label("Add Certification Number")
        certificate.click()
        self.fill_with_effect(certificate, "Updated Certification Number")

        # Update Third Code
        third_code = self.page.get_by_label("Add Third-Code")
        third_code.click()
        self.fill_with_effect(third_code, "Updated Third Code")

        # Toggle Jewelry Certification
        jewelry_certification = self.page.get_by_role("checkbox", name="Add Jewelry Certification")
        self.click_with_effect(jewelry_certification)

        # Toggle Appraisal
        appraisal = self.page.get_by_role("checkbox", name="Add Appraisal")
        self.click_with_effect(appraisal)

        # Add Product Note
        product_note = self.page.get_by_role("checkbox", name="Add To Product Note")
        self.click_with_effect(product_note)

        # Click on UPDATE
        update = self.page.locator("(//span[@class='v-btn__overlay'])[37]")
        self.click_with_effect(update)



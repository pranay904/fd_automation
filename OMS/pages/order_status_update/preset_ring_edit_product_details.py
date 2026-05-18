import random
import time

from service_identity.cryptography import verify_certificate_hostname

from OMS.pages.order_status_update.orderstatusbase import OrderStatusBase


class EditProduct(OrderStatusBase):

    def __init__(self, page):
        super().__init__(page)

    def open_all_order_line(self):
        self.open_order_and_all_order_line()
        self.wait_delay()

    def preset_product(self):
        # Get the current page URL
        current_url = self.page.url

        # Append the parameters directly
        new_url = current_url + "&show_child=false&order_line_type=7"

        print("Navigating to preset product URL:", new_url)

        # Navigate to the new URL
        self.page.goto(new_url)

        panel = self.page.locator(
            "(//span[@class='v-expansion-panel-title__overlay'])[1]"
        )
        self.click_with_effect(panel)



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

        size_options = [
            '3', '3.25', '3.5', '3.75', '4', '4.25', '4.5', '4.75', '5', '5.25', '5.5', '5.75',
            '6', '6.25', '6.5', '6.75', '7', '7.25', '7.5', '7.75', '8', '8.25', '8.5', '8.75',
            '9', '9.25', '9.5', '9.75', '10', '10.25', '10.5', '10.75', '11', '11.25', '11.5', '11.75',
            '12', '12.25', '12.5', '12.75', '13'
        ]

        size_text = self.page.locator("(//div[@class='v-field__input'])[11]")
        size_text.wait_for(state="visible")

        current_size_text = size_text.inner_text().strip()
        print("Current size:", current_size_text)

        size_dropdown = self.page.locator("(//div[@role='combobox'])[10]")
        size_dropdown.wait_for(state="visible")
        self.click_with_effect(size_dropdown)

        if current_size_text in size_options:
            next_size = size_options[(size_options.index(current_size_text) + 1) % len(size_options)]
        else:
            next_size = size_options[0]

        print("Selecting size:", next_size)

        size_option = self.page.locator(
            f"//div[@role='option' and normalize-space()='{next_size}']"
        )

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

        time.sleep(5)

            # verify order logs
        order_log = self.page.get_by_role("button", name="Order-Logs")
        order_log.wait_for(state="visible")
        order_log.scroll_into_view_if_needed()
        self.click_with_effect(order_log)

        verify_recent_logs = self.page.locator("//div[@class='v-card-text']//div[3]")
        verify_recent_logs.wait_for(state="visible")

        self.hover_with_effect(verify_recent_logs)



    # --- Fun 3: Update Mount ---
    def update_mount(self):
        mount = "Studded"
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
        self.fill_with_effect(inscription, "Add Inscription")

        # Update Certificate Number
        certificate = self.page.get_by_label("Add Certification Number")
        certificate.click()
        self.fill_with_effect(certificate, "Enter Certification Number")

        # Update Third Code
        third_code = self.page.get_by_label("Add Third-Code")
        third_code.click()
        self.fill_with_effect(third_code, "Enter The Third Code")

        # Toggle Jewelry Certification
        jewelry_certification = self.page.get_by_role("checkbox", name="Add Jewelry Certification")
        self.click_with_effect(jewelry_certification) # Yes/ NO

        # Toggle Appraisal
        appraisal = self.page.get_by_role("checkbox", name="Add Appraisal")
        self.click_with_effect(appraisal) # $50

        # Add Product Note
        product_note = self.page.get_by_role("checkbox", name="Add To Product Note")
        self.click_with_effect(product_note)

        # Click on UPDATE
        update = self.page.locator(
            "//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']")

        update.wait_for(state="visible")
        update.scroll_into_view_if_needed()
        self.click_with_effect(update)

        verify_inscription = self.page.locator("//p[starts-with(normalize-space(), 'Inscription -')]")
        self.click_with_effect(verify_inscription)
        time.sleep(2)

        verify_appraisal = self.page.locator("//p[starts-with(normalize-space(), 'Appraisal Price -')]")
        self.click_with_effect(verify_appraisal)

        verify_certificate = self.page.locator("//p[starts-with(normalize-space(), 'Certification No -')]")
        self.click_with_effect(verify_certificate)

        verify_third_code = self.page.locator("//p[starts-with(normalize-space(), 'Third Code -')]")
        self.click_with_effect(verify_third_code)

        verify_jewelry_certified = self.page.locator("//p[starts-with(normalize-space(), 'Jewelry-Certified -')]")
        self.click_with_effect(verify_jewelry_certified)



    def add_product_note(self):

        product_note = self.page.locator("//span[normalize-space()='Add-Product-Note']")
        product_note.scroll_into_view_if_needed()

        self.click_with_effect(product_note)

        # enter the product note

        add_note = self.page.get_by_role("textbox", name="Enter Product-Note")
        self.fill_with_effect(add_note, value="Enter Product Note Here & click on update")

        update = self.page.locator("//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']")

        update.wait_for(state="visible")
        update.scroll_into_view_if_needed()
        self.click_with_effect(update)

        verify_the_product_status = self.page.locator("//p[starts-with(normalize-space(), 'Product Status :')]")
        self.hover_with_effect(verify_the_product_status)
        time.sleep(2)


    def edit_product_status(self):
        status_options = ["In Process", "Factory Complete", "Buy From NY"]

        # Open Edit Product Status form
        click_on_link = self.page.locator("//span[normalize-space()='Edit Product Status']")
        self.click_with_effect(click_on_link)

        # Get current status
        text = self.page.locator("(//div[@class='v-field__input'])[11]")
        text.wait_for(state="visible")
        current_status_text = text.inner_text().strip()
        print("Current status:", current_status_text)

        # Open dropdown
        status_dropdown = self.page.locator("(//div[@role='combobox'])[10]")
        status_dropdown.wait_for(state="visible")
        self.click_with_effect(status_dropdown)

        # select next status
        if current_status_text in status_options:
            next_status = status_options[(status_options.index(current_status_text) + 1) % len(status_options)]
        else:
            next_status = status_options[0]

        print("Selecting status:", next_status)

        # Click the option
        option_locator = self.page.locator(f"//div[@role='option' and normalize-space()='{next_status}']")
        option_locator.wait_for(state="visible")
        self.click_with_effect(option_locator)

        update = self.page.locator("//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']")

        update.wait_for(state="visible")
        update.scroll_into_view_if_needed()
        self.click_with_effect(update)


    def edit_manufacture(self):

        # Click "Edit Manufacturer" button
        open_edit_manf = self.page.get_by_text("Edit Manufacturer", exact=True)
        self.click_with_effect(open_edit_manf)

        # Locate the manufacturer dropdown field
        text = self.page.locator("(//div[@class='v-field__input'])[11]")
        text.wait_for(state="visible")
        text.scroll_into_view_if_needed()

        # Get currently selected manufacturer
        current_text = text.inner_text().strip()
        print("current manufacture:", current_text)

        # Open the dropdown
        text.click()

        # Locate all options
        options = self.page.locator("(//div[@role='listbox'])[1]//div[@role='option']")
        all_options = options.all_inner_texts()
        print("All options list:", all_options)

        # Remove the currently selected value
        available_options = []
        for opt in all_options:
            if opt != current_text:
                available_options.append(opt)

        # Pick a different manufacturer randomly
        new_manufacture = random.choice(available_options)
        print("Selecting new manufacture:", new_manufacture)

        # Click the new option using normalize-space() to handle extra spaces
        new_option = self.page.locator(
            f"//div[@role='option'][normalize-space()='{new_manufacture}']"
        )
        new_option.wait_for(state="visible", timeout=5000)  # wait until visible
        self.click_with_effect(new_option)

        update = self.page.locator("//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']")

        update.wait_for(state="visible")
        update.scroll_into_view_if_needed()
        self.click_with_effect(update)



    def edit_setting_status(self):


        # Click "Edit status" button
        open_edit_manf = self.page.get_by_text("Edit Setting Status", exact=True)
        self.click_with_effect(open_edit_manf)

        # Locate the manufacturer dropdown field
        text = self.page.locator("(//div[@class='v-field__input'])[11]")
        text.wait_for(state="visible")
        text.scroll_into_view_if_needed()

        # Get currently selected manufacturer
        current_text = text.inner_text().strip()
        print("current status:", current_text)

        # Open the dropdown
        self.click_with_effect(text)

        # Locate all options
        options = self.page.locator("(//div[@role='listbox'])[1]//div[@role='option']")
        all_options = options.all_inner_texts()
        print("All options list:", all_options)

        #empty list
        available_options = []

        # Remove the currently selected value

        for opt in all_options:
            if opt != current_text:
                available_options.append(opt)

        # Pick a different manufacturer randomly

        new_setting_status = random.choice(available_options)
        print("Selecting new setting status:", new_setting_status)

        # Click the new option using normalize-space() to handle extra spaces
        new_option = self.page.locator(
            f"//div[@role='option'][normalize-space()='{new_setting_status}']"
        )
        new_option.wait_for(state="visible", timeout=5000)  # wait until visible
        self.click_with_effect(new_option)

        update = self.page.locator(
            "//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']")

        update.wait_for(state="visible")
        update.scroll_into_view_if_needed()
        self.click_with_effect(update)

        verify_the_updated_status= self.page.locator("//p[starts-with(normalize-space(), 'Setting Status -')]")
        self.hover_with_effect(verify_the_updated_status)










































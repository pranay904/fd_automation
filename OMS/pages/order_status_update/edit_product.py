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

    def open_the_edit_modal(self):

        # Update Ring Size

        size = "5"

        ring_size_dropdown = self.page.locator("(//label[@id='input-v-0-382-label'])[1]").click()
        self.click_with_effect(ring_size_dropdown)

        size_option = self.page.locator(
            f"//div[@role='option' and normalize-space()='{size}']"
        )
        self.click_with_effect(size_option)

        # Update Mount Status

        mount_status_dropdown = self.page.get_by_label("Mount Status")
        self.click_with_effect(mount_status_dropdown)

        mount_option = self.page.locator("(//div[@role='option'])[2]")
        self.click_with_effect(mount_option)

        # Update Inscription

        inscription = self.page.get_by_label("Add Inscription")
        self.fill_with_effect(inscription, "Test QA Automation")

        # Update Certificate Number

        certificate = self.page.get_by_label("Add Certification Number")
        self.fill_with_effect(
            certificate,
            "Updated Certification Number"
        )

        # Update Certificate Comment

        certificate_comment = self.page.get_by_label("Add Certification Comment")
        self.fill_with_effect(
            certificate_comment,
            "Updated Certification Comment"
        )


        # Update Third Code

        third_code = self.page.get_by_label("Add Third-Code")
        self.fill_with_effect(
            third_code,
            "Updated Third Code"
        )

        # Toggle Jewelry Certification

        jewelry_certification = self.page.get_by_role(
            "checkbox",
            name="Add Jewelry Certification"
        )
        self.click_with_effect(jewelry_certification)
        self.click_with_effect(jewelry_certification)


        # Toggle Appraisal

        appraisal = self.page.get_by_role(
            "checkbox",
            name="Add Appraisal"
        )
        self.click_with_effect(appraisal)
        self.click_with_effect(appraisal)

        # Add Product Note

        product_note = self.page.get_by_role(
            "checkbox",
            name="Add To Product Note"
        )
        self.click_with_effect(product_note)

        # click on update

        update = self.page.locator(":text-is('UPDATE')")
        self.click_with_effect(update)



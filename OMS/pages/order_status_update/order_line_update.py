import time

from OMS.pages.order_status_update.orderstatusbase import OrderStatusBase


class AddDiamondLines(OrderStatusBase):

    def __init__(self, page):
        super().__init__(page)


    # Open All Order Lines


    def open_all_order_line(self):
        self.open_order_and_all_order_line()
        self.wait_delay()

    # Add Diamond Line

    def add_diamond_line(self):

        add_diamond_btn = self.page.get_by_text("Add Diamond-Line", exact=True)
        self.click_with_effect(add_diamond_btn)

        diamond_type_dropdown = self.page.locator("(//div[@class='v-field__input'])[11]")
        self.click_with_effect(diamond_type_dropdown)

        center_option = self.page.get_by_text("Center", exact=True)
        self.click_with_effect(center_option)

        supplier_dropdown = self.page.locator("(//div[@class='v-field__input'])[12]")
        self.click_with_effect(supplier_dropdown)

        supplier_option = self.page.get_by_text("aarush_diam", exact=True)
        self.click_with_effect(supplier_option)

        create_button = self.page.get_by_role("button", name="Create")

        self.click_with_effect(create_button)

    def delete_dia_line(self):
        delete_dia_line = self.page.get_by_text("Delete Diamond Line", exact=True)
        self.click_with_effect(delete_dia_line)

    def delete_diam(self):
        delete_diam = self.page.get_by_text("Delete Diamond", exact=True)
        self.click_with_effect(delete_diam)


    def add_diam_from_inventry(self):
        stock = "D46382"

        text_box = self.page.get_by_role("textbox", name="Enter Lot Number")
        self.fill_with_effect(text_box, stock)

        add_diamond = self.page.locator(
            "//button[@class='v-btn v-btn--slim v-theme--light bg-indigo-darken-3 px-4 v-btn--density-default v-btn--size-default v-btn--variant-flat']"
        )
        self.click_with_effect(add_diamond)

    def edit_dia_status(self):
        self.add_diamond_line()

        self.add_diam_from_inventry()

        edit_dia_status = self.page.get_by_text("Edit Diamond Status", exact=True)
        self.click_with_effect(edit_dia_status)


        text = self.page.locator("(//label[@id='input-v-0-743-label'])[1]")
        current_text= text.inner_text().strip()

        print("Current diamonds status: ", current_text)













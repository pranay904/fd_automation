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


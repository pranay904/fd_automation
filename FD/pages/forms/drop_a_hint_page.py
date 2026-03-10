from FD.components.base_form_page import BaseFormPage
from FD.utils.config import BASE_URL, CYO_R_URL
from playwright.sync_api import expect

class DropHint(BaseFormPage):

    def __init__(self, page):
        super().__init__(page)

    def open_Base_url(self):
        self.page.goto(BASE_URL)

    def navigate_to_pdp(self):

        self.page.goto(CYO_R_URL)

        self.page.locator("(//div[@class='mb-4 jewelry_block col-lg-3 col-md-4 col-6'])[2]").click()

        drop_hint = self.page.locator("div.drop_hint")

        # Validate text
        expect(drop_hint).to_contain_text("Drop a hint")
        # Click
        drop_hint.click()



        # checked - send me the copy
        #self.page.locator("//span[@class='unchecked']").click()










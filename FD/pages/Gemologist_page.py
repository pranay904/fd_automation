from playwright.sync_api import expect

from FD.components.base_form_page import BaseFormPage
from FD.utils.config import CYO_R_URL


class Gemologist(BaseFormPage):

    def __init__(self, page):
        super().__init__(page)


    def naviagate_to_gemo(self):

        self.page.goto(CYO_R_URL)

        self.page.locator("//div[@class='gemo_box d-flex align-items-center']").click()

        gemologist = self.page.locator(".gemo_box.d-flex.align-items-center")

        # Validate text
        expect(gemologist).to_contain_text("Gemologist's Opinion")
        # Click
        gemologist.click()






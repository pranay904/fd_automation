from FD.components.base_form_page import BaseFormPage
from FD.utils.config import BESPOKE_JEWELRY_URL

class Bespoke_Jewelery(BaseFormPage):

    def __init__(self, page):
        super().__init__(page)  # ensures BasePage init runs


    def open_bespoke_jewelery(self):
        self.page.goto(BESPOKE_JEWELRY_URL)


    def submit_bespoke_jewelery(self):
        self.submit_form()









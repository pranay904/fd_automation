from FD.components.base_form_page import BaseFormPage
from FD.utils.config import CONTACT_US_URL

class ContactUsPage(BaseFormPage):

    def __init__(self, page):
        super().__init__(page)  # ensures BasePage init runs

    def open_contact_us(self):
        self.page.goto(CONTACT_US_URL)

    def send(self):
        # Reuse BaseFormPage submit_form method
        self.send()



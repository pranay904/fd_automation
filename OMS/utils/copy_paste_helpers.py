from playwright.sync_api import Page

class CopyPasteHelpers:
    def __init__(self, page: Page):
        self.page = page

    # -----------------------------
    # COPY TEXT FROM ELEMENT
    # -----------------------------
    def copy_text(self, locator: str) -> str:
        """
        Copies text from a given element.
        Args:
            locator (str): Selector of the element to copy
        Returns:
            str: Text content of the element
        """
        element = self.page.locator(locator)
        text = element.inner_text()
        return text.strip()

    # -----------------------------
    # PASTE TEXT INTO INPUT
    # -----------------------------
    def paste_text(self, locator: str, text: str):
        """
        Fills a text input with given text
        Args:
            locator (str): Selector of the input field
            text (str): Text to paste
        """
        self.page.fill(locator, "")  # Clear the field first
        self.page.fill(locator, text)

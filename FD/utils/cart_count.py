import re


class CartCount:

    def __init__(self, page):
        self.page = page


    def get_home_cart_count(self, locator):
        """
        Home page / Listing page navbar cart badge count
        Example:
        1
        """

        try:
            text = self.page.locator(locator).inner_text().strip()

            count = int(text) if text else 0

            print(f"[INFO] Navbar cart count: {count}")

            return count

        except Exception:
            return 0



    def get_listing_cart_count(self, locator):
        """
        Listing page cart badge count
        """

        return self.get_home_cart_count(locator)



    def get_pdp_cart_count(self):
        """
        Product page after Add To Cart.
        Quick cart opens:
        My Shopping Bag (1)
        """

        try:

            self.page.wait_for_function(
                """
                () => {
                    let el =
                    document.querySelector(
                    'h2.font-active.mb-0'
                    );

                    return el &&
                    el.innerText.match(/\\(\\d+\\)/);
                }
                """,
                timeout=15000
            )


            text = self.page.locator(
                "h2.font-active.mb-0"
            ).inner_text()


            return self.extract_number(text)


        except Exception:

            return 0



    def get_quick_cart_count(self, locator):
        """
        Quick cart drawer count
        Example:
        My Shopping Bag (2)
        """

        try:

            text = self.page.locator(
                locator
            ).inner_text()

            count = self.extract_number(text)

            print(
                f"[INFO] Quick cart count: {count}"
            )

            return count


        except Exception:

            return 0



    def get_cart_page_count(self, locator):
        """
        Shopping Bag page count
        Example:
        (1)
        """

        try:

            text = self.page.locator(
                locator
            ).inner_text()

            count = self.extract_number(text)

            print(
                f"[INFO] Shopping bag count: {count}"
            )

            return count


        except Exception:

            return 0



    @staticmethod
    def extract_number(text):

        if not text:
            return 0


        match = re.search(
            r"\((\d+)\)",
            text
        )

        if match:
            return int(match.group(1))


        match = re.search(
            r"\b(\d+)\b",
            text
        )

        if match:
            return int(match.group(1))


        return 0
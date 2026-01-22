from home_page_ele import Guest

class CYO_functional():

    def __init__(self, page ):
        self.page = page

    def validate_Metal_filter(self):

        metal = self.page.locator("(//div[@class='drop_box for_desktop'])[1]")
        metal.click()

        options = metal.locator("(//ul[@class='mb-0'])[2]").All_inner_text()
        print("All Metal Options" + str(options))


class base_pos:
    def __init__(self, page):
        self.page = page


    def open_pos(self):
        self.page.locator(".v-navigation-drawer__content").hover()
        self.page.locator("//div[@class='v-list-item-title'][normalize-space()='Order Lines']").click()
        self.page.locator("(//div[contains(text(),'All Order Lines')])[1]").click()
        self.page.locator("(//span[@class='v-expansion-panel-title__overlay'])[1]").click()


    def store_list(self):

        Ny_store = self.page.locator("(//div[@class='v-card-item'])[1]")
        Ny_store.click()

        Amzazon_store = self.page.locator("(//div[@class='v-card-item'])[2]")
        Amzazon_store.click()

        Etsy_store = self.page.locator("(//div[@class='v-card-item'])[3]")
        Etsy_store.click()

        Etsy_store = self.page.locator("(//div[@class='v-card-item'])[4]")
        Etsy_store.click()

        Walmart_store = self.page.locator("(//div[@class='v-card-item'])[5]")
        Walmart_store.click()





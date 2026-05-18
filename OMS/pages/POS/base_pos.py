
class BasePOS:
    def __init__(self, page):
        self.page = page



    def open_pos(self):
        self.page.locator(".v-navigation-drawer__content").hover()
        self.page.locator("//div[@class='v-list-item-title'][normalize-space()='Order Lines']").click()
        self.page.locator("(//div[contains(text(),'POS')])[1]").click()
       # self.page.locator("(//span[@class='v-expansion-panel-title__overlay'])[1]").click()


    def store_list(self):

        Ny_store = self.page.locator("(//div[@class='v-card-item'])[1]")
        Amzazon_store = self.page.locator("(//div[@class='v-card-item'])[2]")
        Etsy_store = self.page.locator("(//div[@class='v-card-item'])[3]")
        Ebay_store = self.page.locator("(//div[@class='v-card-item'])[4]")
        Walmart_store = self.page.locator("(//div[@class='v-card-item'])[5]")
        return {
            "Ny_store":Ny_store,
            "Amzazon_store":Amzazon_store,
            "Etsy_store":Etsy_store,
            "Ebay_store":Ebay_store,
            "Walmart_store":Walmart_store
        }

    def product_type(self):

        return{
        "In_Stock":self.page.get_by_role("button", name="In Stock"),
        "Cyo":self.page.get_by_role("button", name="Cyo"),
        "Cyo_Ring": self.page.get_by_role("button", name="Ring", exact=True),
        "Cyo_Pendant":self.page.get_by_role("button", name="Pendant", exact=True),
        "Cyo_Earring":self.page.get_by_role("button", name="Earring", exact=True),
        "Diamond":self.page.get_by_role("button", name="DIAMOND"),
        "Preset":self.page.get_by_role("button", name="PRESET"),
        "Jewelry":self.page.get_by_role("button", name="JEWELRY")
        }















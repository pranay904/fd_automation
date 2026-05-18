from FD.pages.home_page_ele import Guest

from FD.pages.base_page import BasePage

def test_home_page(page):

    base_fun = BasePage(page)

    home_page = Guest(page)
    # open the url
    home_page.open_Base_url()

    # click on cyo setting -- Navigation back
    home_page.CYO_Ring()
    base_fun.navigation_Back()


    # click on shop---> navigate back
    home_page.Shop()
    base_fun.navigation_Back()

    # click on  RTS link --> Navigation back
    # from base page
    home_page.RTS()
    base_fun.navigation_Back()












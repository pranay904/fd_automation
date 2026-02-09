from pages.login_page import LoginPage
from pages.order_page import OrderPage
from utils.json_reader import get_login_user

def test_login(page):
    login_page = LoginPage(page)

    # Step 1: Open login page
    login_page.open_login_page()

    # Step 2: Get login credentials from JSON
    login_data = get_login_user()

    # Step 3: Login using credentials
    login_page.login(login_data["email"], login_data["password"])

# Open order page
    order_page = OrderPage(page)
    order_page.open_order()

# search order id

    order_ids = order_page.get_first_n_order_ids(5)

    for order_id in order_ids:
        print(f"Searching Order ID: {order_id}")
        order_page.search_order(order_id)

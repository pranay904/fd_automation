class ProductLocators:

    # Product Information — PDP
    # h1 with class containing 'product' for the product name
    PRODUCT_NAME = "//h1[contains(@class,'product') or contains(@class,'cd_name') or contains(@class,'heading')]"
    # Price — FD uses cd_price or font-active for the selling price
    PRODUCT_PRICE = "(//h4[contains(@class,'cd_price')] | //span[contains(@class,'cd_price')] | //h4[contains(@class,'font-active')] | //span[contains(@class,'font-active')])[1]"
    PRODUCT_MRP = "//span[contains(@class,'plp_mrp_box') or contains(@class,'old_price') or contains(@class,'mrp')]"

    # Metal chips on PDP
    METAL_OPTIONS = "//div[contains(@class,'metal_chip') or contains(@class,'cd_metal_chip')]"
    ACTIVE_METAL = "//div[contains(@class,'metal_chip') and contains(@class,'active')]"

    # Ring Size
    RING_SIZE_DROPDOWN = "//select[contains(@class,'ring_size')]"
    SELECTED_RING_SIZE = "//select[contains(@class,'ring_size')]"

    # Add To Cart
    ADD_TO_CART = "//div[@class='select_button']"

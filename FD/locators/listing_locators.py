class ListingLocators:

    FIRST_PRODUCT = "(//div[contains(@class,'product_box')])[1]//h3/parent::a"
    FIRST_PRODUCT_NAME = "(//div[contains(@class,'product_box')])[1]//h3"
    FIRST_PRODUCT_PRICE = "(//div[contains(@class,'product_box')])[1]//h4"
    FIRST_PRODUCT_MRP = "(//div[contains(@class,'product_box')])[1]//span[contains(@class,'plp_mrp_box')]"

    SECOND_PRODUCT = "(//div[contains(@class,'product_box')])[2]//h3/parent::a"
    SECOND_PRODUCT_NAME = "(//div[contains(@class,'product_box')])[2]//h3"
    SECOND_PRODUCT_PRICE = "(//div[contains(@class,'product_box')])[2]//h4"
    SECOND_PRODUCT_MRP = "(//div[contains(@class,'product_box')])[2]//span[contains(@class,'plp_mrp_box')]"

    THIRD_PRODUCT = "(//div[contains(@class,'product_box')])[3]//h3/parent::a"
    THIRD_PRODUCT_NAME = "(//div[contains(@class,'product_box')])[3]//h3"
    THIRD_PRODUCT_PRICE = "(//div[contains(@class,'product_box')])[3]//h4"
    THIRD_PRODUCT_MRP = "(//div[contains(@class,'product_box')])[3]//span[contains(@class,'plp_mrp_box')]"
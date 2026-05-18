class PriceCalculator:

    @staticmethod
    def clean_price(value: str) -> float:
        """
        Convert '$480' or '$1,200' → 480.0
        """
        return float(value.replace("$", "").replace(",", "").strip())

    @staticmethod
    def calculate_total_price(setting: dict, diamond: dict) -> float:
        setting_price = PriceCalculator.clean_price(setting["price"])
        diamond_price = PriceCalculator.clean_price(diamond["price"])
        return setting_price + diamond_price

    @staticmethod
    def calculate_total_mrp(setting: dict, diamond: dict) -> float:
        setting_mrp = PriceCalculator.clean_price(setting["mrp"])
        diamond_mrp = PriceCalculator.clean_price(diamond["mrp"])
        return setting_mrp + diamond_mrp

    # NEW METHOD
    @staticmethod
    def calculate_saved_amount(total_price: str, total_mrp: str) -> float:
        """
        Calculate saved amount = MRP - Price
        Accepts string like '$915'
        """
        price = PriceCalculator.clean_price(total_price)
        mrp = PriceCalculator.clean_price(total_mrp)

        return mrp - price
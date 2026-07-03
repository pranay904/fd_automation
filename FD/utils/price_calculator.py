class PriceCalculator:

    @staticmethod
    def clean_price(value: str) -> int:
        """
        Convert '$480' or '$1,200' → 480
        """
        return int(
            float(
                value.replace("$", "").replace(",", "").strip()
            )
        )

    @staticmethod
    def calculate_total_price(setting: dict, diamond: dict) -> int:
        setting_price = PriceCalculator.clean_price(setting["price"])
        diamond_price = PriceCalculator.clean_price(diamond["price"])

        return setting_price + diamond_price

    @staticmethod
    def calculate_total_mrp(setting: dict, diamond: dict) -> int:
        setting_mrp = PriceCalculator.clean_price(setting["mrp"])
        diamond_mrp = PriceCalculator.clean_price(diamond["mrp"])

        return setting_mrp + diamond_mrp

    @staticmethod
    def calculate_saved_amount(total_price: str, total_mrp: str) -> int:
        """
        Calculate saved amount = MRP - Price
        Accepts string like '$915'
        """
        price = PriceCalculator.clean_price(total_price)
        mrp = PriceCalculator.clean_price(total_mrp)

        return mrp - price

    @staticmethod
    def calculate_chain_price(
        base_price: int,
        thickness_addon: int,
        discount_amount: int = 0
    ) -> int:
        """
        Calculate final chain price after thickness and discount.

        Formula:
        (Base Price + Thickness Addon) - Discount
        """
        return (base_price + thickness_addon) - discount_amount

    @staticmethod
    def calculate_chain_mrp(
        base_mrp: int,
        thickness_addon: int
    ) -> int:
        """
        Calculate final chain MRP.

        Formula:
        Base MRP + Thickness Addon
        """
        return base_mrp + thickness_addon

    @staticmethod
    def calculate_discount_amount(
        mrp: int,
        selling_price: int
    ) -> int:
        """
        Calculate discount amount.
        """
        return mrp - selling_price

    @staticmethod
    def calculate_discount_percentage(
        mrp: int,
        selling_price: int
    ) -> int:
        """
        Calculate discount percentage.
        """
        if mrp == 0:
            return 0

        discount = mrp - selling_price

        return round((discount / mrp) * 100)
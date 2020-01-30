class Food:
    name = None
    category = None
    price = 0.0
    packing_fee = 0.0
    second_price = 0.0
    applicable_quantity = 0
    no_reduction = False

    def __init__(self, name, category, price, packing_fee, second_price, applicable_quantity, no_reduction):
        self.name = name
        self.category = category
        self.price = price
        self.packing_fee = packing_fee
        self.second_price = second_price
        self.applicable_quantity = applicable_quantity
        self.no_reduction = no_reduction

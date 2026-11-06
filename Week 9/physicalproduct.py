LINE = "-" * 48
BASE_SHIPPING_FEE = 5.00
FEE_PER_KG = 2.00
from product import Product
from canbeshipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock,weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    # ----- Read-only access to attributes -----
    @property
    def weight(self):
        return self.__weight

    # ----- Extended methods -----

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight}")
        print(LINE)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
    
    # ----- Abstract method -----
    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return BASE_SHIPPING_FEE + FEE_PER_KG * self.__weight

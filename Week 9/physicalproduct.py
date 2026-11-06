LINE = "-" * 48
from product import Product

class PhysicalProduct(Product):

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

    # ----- Abstract method -----
    def get_fulfilment_info(self):
        return "This product requires physical shipping."

LINE = "-" * 48
from product import Product

class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    # ----- Read-only access to attributes -----
    @property
    def download_size(self):
        return self.__download_size

    # ----- Extended methods -----

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size}MB")
        print(LINE)

    # ----- Abstract method -----
    def get_fulfilment_info(self):
        return "This product is delivered digitally via download link."

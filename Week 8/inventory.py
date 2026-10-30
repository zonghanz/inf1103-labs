LINE = "-" * 48


class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            print(product)
        print(LINE)

    def get_products(self):
        return list(self.__products)

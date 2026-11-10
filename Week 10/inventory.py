from product import Product

LINE = "-" * 48


# SRP: An Inventory is responsible for managing a collection of Products.
# AGGREGATION: an Inventory holds references to Products but does not create them
# or control their lifecycle. A Product can exist before it is added, can be removed,
# and can be added to another Inventory without being destroyed.
class Inventory:

    def __init__(self) -> None:
        # Typed with the base class Product so it can hold ANY kind of product (LSP).
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        # Returns a copy so outside code cannot change the Inventory's list directly.
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        # Only removes the reference from this Inventory. The Product object lives on.
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        if not self.__products:
            print(LINE)
            print("No products in inventory.")
            print(LINE)
        for product in self.__products:
            product.display_information()   # each product decides how it displays (polymorphism)

LINE = "-" * 48


class Inventory:
    """Manages a collection of Product objects (SRP: the collection, not one product)."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if a product with the same ID already exists."""
        if self.search_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with the given ID (case-insensitive), or None."""
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
        """Return a copy of the product list (so callers can't alter the internal list)."""
        return list(self.__products)

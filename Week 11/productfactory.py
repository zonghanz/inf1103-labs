from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


# FACTORY PATTERN: the one place that decides which Product subclass to build.
# The rest of the program asks the factory for a Product and never calls
# PhysicalProduct(...) or DigitalProduct(...) directly.
# A new product type means changing this class only (one place, not many).
class ProductFactory:

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, weight: float = 0.0,
               download_size: float = 0.0) -> Product:
        # weight is only used by physical products, download_size only by digital ones.
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, weight)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")

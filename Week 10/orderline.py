from product import Product


class OrderLine:
    # One product and the quantity of it requested in ONE order.
    # COMPOSITION: an OrderLine is part of an Order. It is created by Order.add_order_line()
    # and is never created elsewhere or moved to another Order.
    # ASSOCIATION: the OrderLine only refers to its Product. It does not own the Product.

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        self.__product: Product = product
        self.__quantity: int = quantity

    # ----- Read-only access to attributes -----
    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    # ----- Behaviour -----
    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_line(self) -> None:
        print(f"{self.__product.product_id} | {self.__product.name} | "
              f"${self.__product.price:.2f} x {self.__quantity} = "
              f"${self.calculate_subtotal():.2f}")

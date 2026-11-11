from orderline import OrderLine
from product import Product

LINE = "-" * 48

# COMPOSITION
# Order builds an OrderLine and hands it in, so every line belongs to exactly one Order
class Order:

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    # Read-only access to attributes 
    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        # Returns a copy: the Order alone controls which lines it holds.
        return list(self.__order_lines)

    # Behaviour 
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # the Order creates its own part
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        # The removed OrderLine goes away with the order
        for order_line in self.__order_lines:
            if order_line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum((order_line.calculate_subtotal()
                    for order_line in self.__order_lines), 0.0)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(LINE)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_line()
        print(LINE)
        print(f"Total: ${self.calculate_total():.2f}")

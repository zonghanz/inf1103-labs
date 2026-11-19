from orderline import OrderLine
from product import Product
from discountstrategy import DiscountStrategy
from nodiscount import NoDiscount

LINE = "-" * 48

# COMPOSITION
# Order builds an OrderLine and hands it in, so every line belongs to exactly one Order
# ASSOCIATION (Strategy pattern): an Order USES one DiscountStrategy but does not own it.
# The same strategy object can be shared by many orders, and swapped with set_discount().
class Order:

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        # If no strategy is given, the order uses NoDiscount().
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    # Read-only access to attributes 
    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        # Returns a copy: the Order alone controls which lines it holds.
        return list(self.__order_lines)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    # Behaviour 
    def set_discount(self, discount: DiscountStrategy) -> None:
        # Swaps the strategy at runtime; Order itself does not change.
        self.__discount = discount

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
        # No if/elif about discount types: the strategy decides the discounted total.
        total = sum((order_line.calculate_subtotal()
                     for order_line in self.__order_lines), 0.0)
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print(LINE)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_line()
        print(LINE)
        print(f"Discount: {self.__discount}")
        print(f"Total: ${self.calculate_total():.2f}")

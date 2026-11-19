from discountstrategy import DiscountStrategy


class NoDiscount(DiscountStrategy):
    # The default strategy: the total is returned unchanged.

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"

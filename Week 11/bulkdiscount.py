from discountstrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    # Takes a fixed amount off any total at or above the threshold,
    # e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more.

    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold: float = threshold
        self.__amount: float = amount

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total

    def __str__(self) -> str:
        return f"${self.__amount:.2f} off orders of ${self.__threshold:.2f} or more"

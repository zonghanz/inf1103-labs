from discountstrategy import DiscountStrategy

STUDENT_PERCENTAGE = 5


class StudentDiscount(DiscountStrategy):
    # Added in Section 2.4 WITHOUT changing Order: a new option is a new class.
    # Students get a fixed 5% off the total.

    def apply(self, total: float) -> float:
        return total * (1 - STUDENT_PERCENTAGE / 100)

    def __str__(self) -> str:
        return f"Student discount ({STUDENT_PERCENTAGE}% off)"

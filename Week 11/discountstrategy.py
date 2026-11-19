from abc import ABC, abstractmethod


# STRATEGY PATTERN: every discount option is its own class with the same apply() method.
# Order only calls apply(), so it never needs to know which discount it was given.
class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        pass

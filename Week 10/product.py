LINE = "-" * 48
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    # ASSOCIATION: a Product holds a reference to the Supplier that supplied it.

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id             # attributes
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    # Read-only access to attributes 
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # Behaviour
    # a valid quantity (>= 0) replaces the stock,
    # PhysicalProduct and DigitalProduct inherits without changing its meaning.
    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(LINE)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.name} ({self.__supplier.supplier_id})")

    def display_supplier_information(self) -> None:
        # Product asks the Supplier to describe itself.
        self.__supplier.display_information()

    def to_dict(self) -> dict[str, str | int | float]:
        # Only the supplier's ID is saved here; the Supplier is saved separately.
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock,
                "supplier_id": self.__supplier.supplier_id}

    # Abstract behaviour: every subclass MUST implement this 
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def __str__(self) -> str:
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

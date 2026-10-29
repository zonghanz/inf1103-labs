LINE = "-" * 48


class Product:
    """Represents and manages a single product (SRP: one product's data and state)."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ----- Read-only access to attributes -----
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ----- Behaviour -----
    def update_stock(self, quantity):
        """Set the stock level. The Product decides what values are acceptable."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Print the full details of this product."""
        print(LINE)
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(LINE)

    def to_dict(self):
        """Return the product as a plain dict (used by the main program when saving to JSON)."""
        return {"id": self.__product_id, "name": self.__name,
                "price": self.__price, "stock": self.__stock}

    def __str__(self):
        """One-line summary used when listing all products."""
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

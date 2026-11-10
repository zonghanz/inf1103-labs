LINE = "-" * 48


class Supplier:
    # Represents a single supplier (SRP: one supplier's details).
    # ASSOCIATION: a Supplier exists on its own. Products only keep a reference to it,
    # they do not own it, and a Supplier does not need to know about its Products.

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id           # attributes
        self.__name: str = name
        self.__contact_email: str = contact_email

    # ----- Read-only access to attributes -----
    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    # ----- Behaviour -----
    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {"id": self.__supplier_id, "name": self.__name,
                "contact_email": self.__contact_email}

    def __str__(self) -> str:
        return f"{self.__supplier_id} | {self.__name} | {self.__contact_email}"

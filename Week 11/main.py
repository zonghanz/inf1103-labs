import csv
import json
import os

from inventory import Inventory
from order import Order
from discountstrategy import DiscountStrategy
from nodiscount import NoDiscount
from percentagediscount import PercentageDiscount
from bulkdiscount import BulkDiscount
from studentdiscount import StudentDiscount
from product import Product
from productfactory import ProductFactory
from supplier import Supplier
from canbeshipped import CanBeShipped

INVENTORY_FILE = "inventory.json"
PRODUCTS_FILE = "products.csv"

# Used when loading a Week 9 style file, where products had no supplier saved.
DEFAULT_SUPPLIER = Supplier("S000", "Unknown Supplier", "not-provided@example.com")


# ===== Product creation from saved data =====
def product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    # Looks up the (already existing) Supplier from the saved supplier_id, then
    # asks the ProductFactory to build the correct subclass from the "type" identifier.
    supplier_id = item.get("supplier_id", DEFAULT_SUPPLIER.supplier_id)
    if supplier_id == DEFAULT_SUPPLIER.supplier_id:
        suppliers.setdefault(supplier_id, DEFAULT_SUPPLIER)
    supplier = suppliers[supplier_id]
    return ProductFactory.create(item["type"], item["id"], item["name"], item["price"],
                                 item["stock"], supplier,
                                 weight=item.get("weight", 0.0),
                                 download_size=item.get("download_size", 0.0))


# ===== File Handling =====
def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory, suppliers

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        if isinstance(data, list):          # Week 9 format: a plain list of products
            supplier_items, product_items = [], data
        else:                               # Week 10 format: suppliers + products
            supplier_items, product_items = data["suppliers"], data["products"]
        for item in supplier_items:
            supplier = Supplier(item["id"], item["name"], item["contact_email"])
            suppliers[supplier.supplier_id] = supplier
        for item in product_items:
            inventory.add_product(product_from_dict(item, suppliers))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError):
        print("File could not be read. Starting with an empty inventory.")
        return Inventory(), {}
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier],
                   on_exit: bool = False) -> None:
    print("\nSaving inventory before exit..." if on_exit else "\nSaving inventory...")
    data = {"suppliers": [supplier.to_dict() for supplier in suppliers.values()],
            "products": [product.to_dict() for product in inventory.products]}
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except OSError:    # e.g. no permission to write the file
        print(f"Inventory could not be saved to {INVENTORY_FILE}.")
        return
    if on_exit:
        print("Inventory saved successfully.")
    else:
        print(f"Inventory saved successfully to {INVENTORY_FILE}.")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    # Reads products from a CSV file and creates each one through the ProductFactory.
    # One bad row is reported and skipped; the valid rows still load.
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)                          # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock), supplier)
                except ValueError as error:
                    print(f"Skipped line {line_number} {row}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipped line {line_number} {row}: "
                          f"product ID {product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


# ===== Menu and User Input =====
def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Load Products from CSV")
    print("9. Exit")
    print("----------------------------\n")


def get_positive_float(prompt: str) -> float:
    # Keeps asking until the user enters a number greater than zero.
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    # Same idea for whole numbers such as a stock quantity (0 or more).
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number of 0 or more.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number, e.g. 10")


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    # Picks an existing Supplier, or creates a new one that exists independently
    # of any product. Returns None if the details entered are invalid.
    print("\nSuppliers:")
    if not suppliers:
        print("(none yet)")
    for supplier in suppliers.values():
        print(supplier)
    supplier_id = input("Supplier ID (existing, or a new ID to create one): ").strip().upper()
    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        return suppliers[supplier_id]

    print(f"Creating new supplier {supplier_id}.")
    name = input("Supplier Name: ").strip()
    email = input("Contact Email: ").strip()
    if not name or "@" not in email:
        print("Supplier name cannot be empty and email must contain '@'.")
        return None
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("Product type:")
    print("1. Physical")
    print("2. Digital")
    type_choice = input("Choose type (1/2): ").strip()
    product_types = {"1": "physical", "2": "digital"}
    if type_choice not in product_types:
        print("Invalid product type. Product not added.")
        return
    product_type = product_types[type_choice]

    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.find_product(product_id):
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    # The helpers keep asking until the input is valid, so no data is left incomplete.
    weight, download_size = 0.0, 0.0
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download size (MB): ")

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Product not added.")
        return

    # The factory decides which subclass to create; main only knows about Product.
    try:
        product = ProductFactory.create(product_type, product_id, name, price, stock,
                                        supplier, weight=weight, download_size=download_size)
    except ValueError as error:    # e.g. "Price must be greater than zero."
        print(f"{error} Product not added.")
        return
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not updated.")
        return
    try:
        product.update_stock(new_stock)
    except ValueError as error:
        print(f"{error} Stock not updated.")
        return
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    product.display_information()
    print(product.get_fulfilment_info())
    # Only products that implement CanBeShipped have a shipping cost.
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("\nSupplier Details")
    product.display_supplier_information()


def remove_product(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from the inventory.")
    else:
        print("Product not found.")


def choose_discount() -> DiscountStrategy:
    # The menu picks WHICH strategy object to create. Order itself never checks
    # the discount type: it only calls apply() on whatever strategy it is given.
    print("\nDiscount:")
    print("1. No discount")
    print("2. Percentage discount (10% off)")
    print("3. Bulk discount ($20 off orders of $200 or more)")
    print("4. Student discount (5% off)")
    choice = input("Choose discount (1-4): ").strip()
    if choice == "2":
        return PercentageDiscount(10)
    if choice == "3":
        return BulkDiscount(200, 20)
    if choice == "4":
        return StudentDiscount()
    if choice != "1":
        print("Invalid choice. No discount applied.")
    return NoDiscount()


def create_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order_id = input("Order ID: ").strip().upper()
    if not order_id:
        print("Order ID cannot be empty.")
        return
    order = Order(order_id)    # the Order creates its own OrderLine objects
    print("Add items to the order. Press Enter on Product ID to finish.")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
            order.add_order_line(product, quantity)
        except ValueError:
            print("Quantity must be a whole number greater than 0. Item not added.")
            continue
        print(f"Added {quantity} x {product.name}.")
    if not order.order_lines:
        print("No items added. Order not created.")
        return
    order.set_discount(choose_discount())    # Strategy chosen at runtime
    order.display_order()


def import_products(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nLoad Products from CSV")
    path = input(f"CSV file path (press Enter for {PRODUCTS_FILE}): ").strip() or PRODUCTS_FILE
    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("No products loaded.")
        return
    load_products(path, inventory, supplier)


# ===== Main Program =====
def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory, suppliers = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            remove_product(inventory)
        elif choice == "6":
            create_order(inventory)
        elif choice == "7":
            save_inventory(inventory, suppliers)
        elif choice == "8":
            import_products(inventory, suppliers)
        elif choice == "9":
            save_inventory(inventory, suppliers, on_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()

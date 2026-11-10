import json
import os

from inventory import Inventory
from order import Order
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from product import Product
from supplier import Supplier
from canbeshipped import CanBeShipped

INVENTORY_FILE = "inventory.json"

# Used when loading a Week 9 style file, where products had no supplier saved.
DEFAULT_SUPPLIER = Supplier("S000", "Unknown Supplier", "not-provided@example.com")


# ===== Product creation from saved data =====
def product_from_dict(item: dict, suppliers: dict[str, Supplier]) -> Product:
    # Uses the "type" identifier to build the correct subclass, and the saved
    # supplier_id to look up the (already existing) Supplier object.
    kind = item["type"]
    supplier_id = item.get("supplier_id", DEFAULT_SUPPLIER.supplier_id)
    if supplier_id == DEFAULT_SUPPLIER.supplier_id:
        suppliers.setdefault(supplier_id, DEFAULT_SUPPLIER)
    supplier = suppliers[supplier_id]
    if kind == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], supplier, item["weight"])
    if kind == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], supplier, item["download_size"])
    raise ValueError(f"Unknown product type: {kind}")


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
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    if on_exit:
        print("Inventory saved successfully.")
    else:
        print(f"Inventory saved successfully to {INVENTORY_FILE}.")


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
    print("8. Exit")
    print("----------------------------\n")


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
    product_type = input("Choose type (1/2): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type. Product not added.")
        return

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
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            extra = float(input("Weight (kg): "))
        else:
            extra = float(input("Download size (MB): "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return
    if price < 0 or stock < 0 or extra < 0:
        print("Values cannot be negative! Product not added.")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Product not added.")
        return

    if product_type == "1":
        product = PhysicalProduct(product_id, name, price, stock, supplier, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, supplier, extra)
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
    order.display_order()


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
            save_inventory(inventory, suppliers, on_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()

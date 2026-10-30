import json
import os

from product import Product
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


# ===== File Handling =====
def load_inventory():
    inventory = Inventory()
    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
        return inventory

    print(f"{INVENTORY_FILE} found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            inventory.add_product(
                Product(item["id"], item["name"], item["price"], item["stock"]))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, OSError, KeyError, TypeError):
        print("File could not be read. Starting with an empty inventory.")
        return Inventory()
    return inventory


def save_inventory(inventory, on_exit=False):
    print("\nSaving inventory before exit..." if on_exit else "\nSaving inventory...")
    data = [product.to_dict() for product in inventory.get_products()]
    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)
    if on_exit:
        print("Inventory saved successfully.")
    else:
        print(f"Inventory saved successfully to {INVENTORY_FILE}.")


# ===== Menu and User Input =====
def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------\n")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id):
        print("A product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative. Product not added.")
        return

    inventory.add_product(Product(product_id, name, price, stock))
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
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


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    product.display_information()


# ===== Main Program =====
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory, on_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

import ast
import json
import os
INVENTORY_FILE = "inventory.json"
LINE = "-" * 48


# ===== Functions =====
def show_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("---------------------------")

def load_inventory():
    """Load inventory from JSON if the file exists, else return an empty list."""
    if os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} found.")
        try:
            with open(INVENTORY_FILE, "r") as f:
                inventory = json.load(f)
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, OSError):
            print("File could not be read. Starting with an empty inventory.")
            return []
    print(f"{INVENTORY_FILE} not found. Starting with an empty inventory.")
    return []

def save_inventory(inventory, on_exit=False):
    """Write the inventory list to JSON."""
    if on_exit:
        print("Saving inventory before exit...")
    else:
        print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)
    if on_exit:
        print("Inventory saved successfully.")
    else:
        print(f"Inventory saved successfully to {INVENTORY_FILE}.")

def find_product(inventory, product_id):
    """Return the product dict with the given ID (case-insensitive), or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None

def display_all(inventory):
    print("Current Inventory")
    print(LINE)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print(LINE)

def add_product(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if find_product(inventory, product_id):
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
    inventory.append({"id": product_id, "name": name,
                      "price": price, "stock": stock})
    print("Product added successfully!")

def update_stock(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not updated.")
        return
    if new_stock < 0:
        print("Stock cannot be negative. Stock not updated.")
        return
    product["stock"] = new_stock
    print("Stock updated successfully!")

def search_product(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)



 #=== Old ===
def get_valid_input():
    product_name = input("\nEnter Product Name. Enter 'quit' to exit:")
    if (product_name == "quit"):
        return product_name, None
    
    stock_quantity = input("Enter stock quantity. Enter 'quit' to exit:")
    if (stock_quantity == "quit"):
        return None, stock_quantity
    
    elif (stock_quantity.isdigit() == False):
        print("Enter a positive integer")
        return None, None
    
    elif (int(stock_quantity) == 0):
        print("Enter a value greater than 0")
        return None, None
    
    else:
        return product_name, int(stock_quantity)


def update_history(history, product_name, stock_quantity):
    if history == []:
        newEntry = [1001, product_name, stock_quantity]
        history.append([1001, product_name, stock_quantity])
        print("\nNew Order Added:")
        print(*newEntry, sep=", ")
        return history
    else:
        latest_index = history[-1][0]
        newEntry = [latest_index + 1, product_name, stock_quantity]
        history.append(newEntry)
        print("\nNew Order Added:")
        print(*newEntry, sep=", ")
        return history


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
 
    while True:
        show_menu()
        choice = input("Enter option: ").strip()
        if choice == "1":
            return;
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory, on_exit=True)
        elif choice == "6":
            save_inventory(inventory, on_exit=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


# ===== Main Program =====
main();
import ast
import json
import os
INVENTORY_FILE = "inventory.json"
inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
]



# ===== Functions =====
def show_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

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
            return;
        elif choice == "3":
            return;
        elif choice == "4":
            return;
        elif choice == "5":
            return;
        elif choice == "6":
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


# ===== Main Program =====
# inventory, history = load_inventory()
loop = True
failed = 0
# print_inventory(history)

main();



# while loop:
#     product_name, stock_quantity= get_valid_input()
#     if (product_name == "quit" or stock_quantity == "quit"):
#         save_inventory(inventory, history)
#         generate_report(inventory, failed)
#         break

#     elif (stock_quantity == None):
#         failed += 1

#     else: #user's value is valid
#         inventory = process_delivery(inventory, stock_quantity)
#         history = update_history(history, product_name, stock_quantity)
#         if inventory > 500:
#             print("Alert! Overstock!")
#             save_inventory(inventory, history)
#             break


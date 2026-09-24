import ast
# ===== Functions =====
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

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax = amount * 0.1
    return tax

def generate_report(total_units, failed_attempts):
    print("Total units processed: ", total_units, "\nTotal number of failed/rejected entries: ", failed_attempts)
    return

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            inventory = int(file.readline())
            history = ast.literal_eval(file.readline())
            return inventory, history
    except FileNotFoundError:
        return 0, []

def save_inventory(inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory) + "\n")
        file.write(str(history) + "\n")
        print("Order successfully saved to inventory.txt")

def update_history(history, product_name, stock_quantity):
    if history == []:
        history.append([1001, product_name, stock_quantity])
        return history
    else:
        latest_index = history[-1][0]
        newEntry = [latest_index + 1, product_name, stock_quantity]
        history.append(newEntry)
        print("\nNew Order Added:")
        print(*newEntry, sep=", ")
        print("\n")
        return history

def print_inventory(history):
    print("Current Orders: \n")
    for transaction in history:
        print(*transaction, sep=", ")
    return

# ===== Main Program =====
inventory, history = load_inventory()
loop = True
failed = 0
print_inventory(history)

while loop:
    product_name, stock_quantity= get_valid_input()
    if (product_name == "quit" or stock_quantity == "quit"):
        generate_report(inventory, failed)
        break

    elif (stock_quantity == None):
        failed += 1

    else: #user's value is valid
        inventory = process_delivery(inventory, stock_quantity)
        history = update_history(history, product_name, stock_quantity)
        save_inventory(inventory, history)
        if inventory > 500:
            print("Alert! Overstock!")
            break


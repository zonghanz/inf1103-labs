import ast
# ===== Functions =====
def get_valid_input():
    stock_quantity = input("Enter stock quantity. Enter 'quit' to exit:")
    if (stock_quantity == "quit"):
        return stock_quantity
    
    elif (stock_quantity.isdigit() == False):
        print("Enter a positive integer")
        return None
    
    elif (int(stock_quantity) == 0):
        print("Enter a value greater than 0")
        return None
    
    else:
        return int(stock_quantity)

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

# ===== Main Program =====
inventory, history = load_inventory()
loop = True
failed = 0
print(inventory,history)

while loop:
    stock_quantity= get_valid_input()
    if (stock_quantity == "quit"):
        generate_report(inventory, failed)
        break

    elif (stock_quantity == None):
        failed += 1

    else: #user's value is valid
        inventory = process_delivery(inventory, stock_quantity)

        if inventory > 500:
            print("Alert! Overstock!")
            break


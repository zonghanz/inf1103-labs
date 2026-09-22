inventory = 0
loop = True
failed = 0

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



    

# ===== Main Program =====
while loop:
    stock_quantity= get_valid_input()
    if (stock_quantity == "quit"):
        print("Total units processed: ", inventory, "\nTotal number of failed/rejected entries: ", failed)
        break

    elif (stock_quantity == None):
        failed += 1

    else: #user's value is valid
        inventory = process_delivery(inventory, stock_quantity)

        if inventory > 500:
            print("Alert! Overstock!")
            break


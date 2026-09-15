inventory = 0
loop = True
failed = 0
total_units = 0

while loop:
    stock_quantity = input("Enter stock quantity. Enter 'quit' to exit:")
    if (stock_quantity == "quit"):
        print("Total units processed: ", total_units, "\nTotal number of failed/rejected entries: ", failed)
        break
    elif (stock_quantity.isdigit() == False):
        print("Enter an integer")
        failed += 1
    elif (int(stock_quantity) < 0):
        print("Do not enter negative numbers")
        failed += 1
    else:
        inventory += int(stock_quantity)
        total_units += 1
        if inventory > 500:
            print("Alert! Overstock!")
            break


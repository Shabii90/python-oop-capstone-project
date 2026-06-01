#===The beginning of the class===
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        # Initialise attributes
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        # Return the cost of the shoe
        return self.cost

    def get_quantity(self):
        # Return the quantity of the shoe
        return self.quantity

    def __str__(self):
        # String representation of Shoe object
        return (f"Country: {self.country}\n"
                f"Code: {self.code}\n"
                f"Product: {self.product}\n"
                f"Cost: {self.cost}\n"
                f"Quantity: {self.quantity}\n")


#===Shoe list===
shoe_list = []


#===Helper function===
def write_shoes_data_to_file():
    """
    Rewrite inventory.txt using the current shoe_list.
    Keeps the header line.
    """
    try:
        with open("inventory.txt", "w", encoding="utf-8") as f:
            f.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in shoe_list:
                f.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
    except Exception as e:
        print("Error writing to inventory.txt:", e)


#===Functions outside the class===
def read_shoes_data():
    """
    Open inventory.txt, read the data, create Shoe objects, append to shoe_list.
    Uses try-except for error handling. Skips the first line (header).
    """
    shoe_list.clear()

    try:
        with open("inventory.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Skip header
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 5:
                print("Skipping invalid line:", line)
                continue

            country, code, product, cost, quantity = parts

            try:
                cost = float(cost)
                quantity = int(quantity)
            except ValueError:
                print("Skipping line with invalid cost/quantity:", line)
                continue

            shoe_list.append(Shoe(country, code, product, cost, quantity))

        print("Shoes data loaded successfully.")

    except FileNotFoundError:
        print("Error: inventory.txt was not found.")
    except Exception as e:
        print("Error reading inventory.txt:", e)


def capture_shoes():
    """
    Allow user to capture shoe data and add a Shoe object to shoe_list.
    """
    country = input("Enter country: ").strip()
    code = input("Enter shoe code: ").strip()
    product = input("Enter product name: ").strip()

    while True:
        try:
            cost = float(input("Enter cost: "))
            break
        except ValueError:
            print("Invalid cost. Please enter a number.")

    while True:
        try:
            quantity = int(input("Enter quantity: "))
            break
        except ValueError:
            print("Invalid quantity. Please enter a whole number.")

    shoe_list.append(Shoe(country, code, product, cost, quantity))
    write_shoes_data_to_file()
    print("Shoe added successfully and saved to inventory.txt.")


def view_all():
    """
    Iterate over shoe_list and print details using __str__.
    """
    if not shoe_list:
        print("No shoes to display. Please load data first.")
        return

    for shoe in shoe_list:
        print(shoe)
        print("-" * 30)


def re_stock():
    """
    Find the shoe with the lowest quantity.
    Ask user if they want to add quantity and update inventory.txt.
    """
    if not shoe_list:
        print("No shoes loaded. Please load data first.")
        return

    lowest_shoe = min(shoe_list, key=lambda s: s.quantity)

    print("\nLowest stock item:")
    print(lowest_shoe)

    choice = input("Do you want to add stock to this item? (yes/no): ").lower().strip()
    if choice != "yes":
        print("Restock cancelled.")
        return

    while True:
        try:
            add_qty = int(input("How many units would you like to add?: "))
            if add_qty < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Invalid number. Please enter a whole number.")

    lowest_shoe.quantity += add_qty
    write_shoes_data_to_file()
    print("Stock updated successfully and saved to inventory.txt.")


def search_shoe():
    """
    Search for a shoe using shoe code and print the found shoe.
    """
    if not shoe_list:
        print("No shoes loaded. Please load data first.")
        return

    code = input("Enter the shoe code to search: ").strip()

    for shoe in shoe_list:
        if shoe.code == code:
            print("\nShoe found:")
            print(shoe)
            return shoe

    print("No shoe found with that code.")
    return None


def value_per_item():
    """
    Calculate and print value for each shoe: cost * quantity.
    """
    if not shoe_list:
        print("No shoes loaded. Please load data first.")
        return

    print("\nValue per item (cost * quantity):")
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"{shoe.product} ({shoe.code}) value: {value}")
    print()


def highest_qty():
    """
    Determine the product with the highest quantity and print it as being for sale.
    """
    if not shoe_list:
        print("No shoes loaded. Please load data first.")
        return

    highest_shoe = max(shoe_list, key=lambda s: s.quantity)

    print("\nProduct with the highest quantity (FOR SALE):")
    print(highest_shoe)


#====Main Menu====
read_shoes_data()  # load automatically at start

while True:
    print("\n=== INVENTORY MENU ===")
    print("1 - Read shoes data (reload from file)")
    print("2 - Capture a new shoe")
    print("3 - View all shoes")
    print("4 - Restock (lowest quantity)")
    print("5 - Search shoe by code")
    print("6 - Value per item")
    print("7 - Highest quantity (for sale)")
    print("8 - Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        read_shoes_data()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        view_all()
    elif choice == "4":
        re_stock()
    elif choice == "5":
        search_shoe()
    elif choice == "6":
        value_per_item()
    elif choice == "7":
        highest_qty()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please choose a number from 1 to 8.")

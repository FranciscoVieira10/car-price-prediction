# Validate integer inputs
def ask_integer(message, minimum=0):
    while True:
        try:
            number = int(input(message))

            if number >= minimum:
                return number

            print(f"Please enter a number greater than or equal to {minimum}.")

        except ValueError:
            print("Please enter a valid integer.")


# Display available options and validate the selection
def ask_option(message, options):
    print(f"\n{message}:")

    for i in range(len(options)):
        print(f"{i + 1}. {options[i]}")

    while True:
        try:
            choice = int(input("Choose an option: "))

            if 1 <= choice <= len(options):
                return options[choice - 1]

            print("Please choose a number from the list.")

        except ValueError:
            print("Please enter a valid number.")

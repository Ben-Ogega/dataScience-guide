import random  # To generate random values for rows and columns in the slot machine

# Global constants (could be moved to a dedicated constants file)
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbol frequency and value dictionaries
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_values = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}


def check_winnings(columns, lines, bet, values):
    """
    Check if there are any winning lines in the given slot machine spin.

    Args:
        columns: A list of lists representing the symbols on the reels.
        lines: The number of lines bet on.
        bet: The amount bet per line.
        values: A dictionary mapping symbols to their payout values.

    Returns:
        A tuple of (total winnings, winning lines).
    """

    winnings = 0
    winning_lines = []
    for line in range(lines):  # Iterate through each line bet on
        symbol = columns[0][line]  # Check the first symbol on the line
        for column in columns:  # Check if all symbols on the line match
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break  # Not a winning line if symbols don't match
        else:  # All symbols on the line match
            winnings += values[symbol] * bet  # Add winnings for this line
            winning_lines.append(line + 1)  # Track the winning line number

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generate a random spin of the slot machine reels.

    Args:
        rows: The number of rows in the slot machine.
        cols: The number of columns in the slot machine.
        symbols: A dictionary mapping symbols to their frequencies.

    Returns:
        A list of lists representing the symbols on the reels.
    """

    all_symbols = []
    for symbol, count in symbols.items():  # Create a list of all symbols
        for _ in range(count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):  # Create each reel
        column = []
        current_symbols = all_symbols[:]  # Copy all symbols for this reel
        for _ in range(rows):  # Fill the reel with random symbols
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns


def print_slot_machine(columns):
    """
    Print the current state of the slot machine reels.

    Args:
        columns: A list of lists representing the symbols on the reels.
    """

    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")  # Print each symbol with separators
            else:
                print(column[row], end="")  # Print last symbol without separator
        print()  # Move to the next line after each row


def deposit():
    """
    Prompt the user for a deposit amount and validate it.

    Returns:
        The deposited amount as an integer.
    """

    while True:
        amount = input("What would you like to deposit? $ ")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.\n")
        else:
            print("Please enter a number. \n")


def get_number_of_lines():
    while True:
        lines = input(
            "Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")

    return lines

def get_bet():
    """
    Prompt the user for a bet amount per line and validate it.

    Returns:
        The bet amount as an integer.
    """
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")

    return amount

def spin(balance):
    """
    Performs a single spin of the slot machine game, including:

    - Getting the number of lines to bet on from the user.
    - Getting the bet amount per line from the user.
    - Validating the bet amount against the user's balance.
    - Spinning the reels and displaying the results.
    - Calculating winnings based on the symbols and bet amount.
    - Updating the user's balance based on the win/loss.

    Args:
        balance (int): The user's current balance.

    Returns:
        int: The difference between the winnings and the total bet for this spin.
    """

    # Get the number of lines to bet on (validated in get_number_of_lines)
    lines = get_number_of_lines()

    # Get the bet amount per line (validated in get_bet)
    bet = get_bet()

    # Calculate the total bet amount
    total_bet = bet * lines

    # Check if the user has enough balance for the bet
    if total_bet > balance:
        print(f"Insufficient funds! Your current balance is ${balance}.")
        return 0  # Indicate no spin happened

    # Inform the user about their bet
    print(f"You are betting ${bet} on {lines} lines. Total bet: ${total_bet}")

    # Spin the reels and get the symbols
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

    # Display the reels for visual representation
    print_slot_machine(slots)

    # Calculate winnings based on symbols, lines, bet, and symbol values
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)

    # Print the winnings and winning lines
    print(f"You won ${winnings}.")
    if winning_lines:
        print(f"You won on lines:", *winning_lines)
    else:
        print("No winning lines this time.")

    # Update the user's balance based on the win/loss
    balance -= total_bet  # Deduct the bet amount
    balance += winnings    # Add the winnings

    return winnings - total_bet  # Return the net change in balance


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}")
if __name__ == '__main__':
    main()
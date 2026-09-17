"""
Simple Calculator
------------------
Asks for two numbers and an operation (+, -, *, /), does the math,
and lets the player calculate again and again until they choose to quit.

This uses variables, input(), int()/float() conversion, if/elif/else,
and a while loop - all things covered in Lessons 2-5.

We also use try/except as a "safety net" - it's not fully taught yet in the
lessons, but we use it here just to catch a division-by-zero or a typo
(like typing letters instead of numbers) so the program doesn't crash.
Think of try/except like a safety net under a trapeze artist: if something
goes wrong, it catches the fall gently instead of letting the program crash!
"""

print("=== Welcome to the Simple Calculator! ===")
print("Enter two numbers and an operation (+, -, *, /) to get an answer.")
print("Type 'quit' at any time when asked for the first number to stop.")
print()

keep_going = True

while keep_going:
    first_input = input("Enter the first number (or 'quit' to stop): ")

    if first_input.lower() == "quit":
        keep_going = False
    else:
        # Safety net: make sure the first number is really a number.
        try:
            first_number = float(first_input)
        except ValueError:
            print("That doesn't look like a number. Let's try again!")
            print()
            continue

        second_input = input("Enter the second number: ")

        # Safety net: make sure the second number is really a number too.
        try:
            second_number = float(second_input)
        except ValueError:
            print("That doesn't look like a number. Let's try again!")
            print()
            continue

        operation = input("Choose an operation (+, -, *, /): ")

        if operation == "+":
            result = first_number + second_number
            print(f"{first_number} + {second_number} = {result}")
        elif operation == "-":
            result = first_number - second_number
            print(f"{first_number} - {second_number} = {result}")
        elif operation == "*":
            result = first_number * second_number
            print(f"{first_number} * {second_number} = {result}")
        elif operation == "/":
            # Safety net: dividing by zero would normally crash the program,
            # so we catch that here and give a friendly message instead.
            try:
                result = first_number / second_number
                print(f"{first_number} / {second_number} = {result}")
            except ZeroDivisionError:
                print("Whoops! We can't divide by zero. Let's try a different number.")
        else:
            print("Hmm, that's not an operation I know. Please use +, -, * or /.")

        print()
        again = input("Do you want to calculate again? (yes/no) ")
        if again.lower() != "yes":
            keep_going = False

        print()

print("Thanks for using the Simple Calculator! Bye for now! 👋")

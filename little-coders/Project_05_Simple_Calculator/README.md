# Project 05: Simple Calculator ➕➖✖️➗

## What This Project Is

A calculator that asks for two numbers and an operation, does the math, handles division by zero gracefully, and lets the player calculate again and again until they choose to quit.

## What It Uses (from Lessons 1-5)

- Variables to store numbers and results
- `input()` to ask for numbers and the operation
- `float()` conversion to turn text into real numbers for math
- `if`/`elif`/`else` to pick the right operation
- A `while` loop so the player can calculate multiple times
- `try`/`except` as a simple "safety net" (explained in a code comment) to catch division-by-zero and non-numeric typos gracefully instead of crashing

## How to Run It

1. Open `simple_calculator.py` in Thonny or Repl.it.
2. Press Run (or F5).
3. Type a number, then a second number, then an operation (`+`, `-`, `*`, or `/`).
4. See your answer! Choose to calculate again, or type "quit" to stop.

## Files

- `simple_calculator.py` — the full calculator program
- `Teacher_Guide.md` — how to use this with students
- `Student_Guide.md` — instructions written for kids
- `assets/` — supporting files (currently empty)

## Example Run (Real Captured Transcript)

This is a real transcript captured by running the script with `subprocess` and simulated input, showing a normal calculation, a non-numeric typo being caught gracefully, and a division-by-zero being caught gracefully:

```
=== Welcome to the Simple Calculator! ===
Enter two numbers and an operation (+, -, *, /) to get an answer.
Type 'quit' at any time when asked for the first number to stop.

Enter the first number (or 'quit' to stop): Enter the second number: Choose an operation (+, -, *, /): 12.0 + 4.0 = 16.0

Do you want to calculate again? (yes/no) 
Enter the first number (or 'quit' to stop): That doesn't look like a number. Let's try again!

Enter the first number (or 'quit' to stop): Enter the second number: That doesn't look like a number. Let's try again!

Enter the first number (or 'quit' to stop): Enter the second number: Choose an operation (+, -, *, /): Whoops! We can't divide by zero. Let's try a different number.

Do you want to calculate again? (yes/no) 
Thanks for using the Simple Calculator! Bye for now! 👋
```

The simulated inputs used for this run were: `12`, `4`, `+`, `yes`, `abc` (typo, non-numeric — caught gracefully), `10`, `yes`, `10`, `0`, `/` (division by zero — caught gracefully), `no`.

The program completed with `returncode == 0` and no traceback or unhandled exception at any point.

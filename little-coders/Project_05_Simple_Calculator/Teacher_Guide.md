# Teacher Guide: Project 05 — Simple Calculator

## Purpose
This project reinforces variables, input, number conversion, if/elif/else, and while loops from Lessons 2-5. It also gently introduces `try`/`except` as a "safety net" concept, explained in a plain-language code comment, without requiring deep understanding of exception handling.

## Suggested Use
- Run the calculator together as a class first, trying each operation.
- Deliberately trigger the division-by-zero case and a non-numeric input to show students the program does NOT crash — point out the friendly message instead of a red error.
- Have students explain in their own words why we need `float()` around the input before doing math.

## What to Look For
- Do students understand that `input()` always gives text, and `float()` turns it into a number?
- Can students trace through the `while` loop and explain when it stops (when the player types "quit" or answers "no" to play again)?
- Do students notice the `try`/`except` blocks and can they explain, simply, what a "safety net" does?

## Common Issues Students May Hit
- Confusing `int()` and `float()` — this project uses `float()` so it can handle decimals too.
- Trying to remove the `try`/`except` "safety net" and then being surprised when a typo crashes the program — this is a great teaching moment about why safety nets matter.
- Forgetting to type "quit" or "no" correctly (case matters unless using `.lower()`, which this program already handles for "quit" and "yes"/"no").

## Extension Ideas
- Add a new operation like `**` for exponents (advanced, optional).
- Have students add a running history of all calculations performed during one session, printed at the end (requires a list, previewed in Lesson 6).

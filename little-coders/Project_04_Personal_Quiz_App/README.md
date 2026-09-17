# Project 04: Personal Quiz App 🧠🎉

## What This Project Is

A friendly, interactive quiz game! It asks the player's name, then asks 5 fun questions — a mix of general-knowledge and "about you" questions — keeps track of a real score, and gives a friendly final message based on how well they did.

## What It Uses (from Lessons 1-7)

- Variables (`score`, `name`, `answerN`)
- `input()` to ask questions
- f-strings for friendly, personalized messages
- `if`/`elif`/`else` to check answers and give tiered feedback
- Simple counting logic (`score = score + 1`)

## How to Run It

1. Open `personal_quiz_app.py` in Thonny or Repl.it.
2. Press Run (or F5).
3. Answer each question in the shell when prompted.
4. See your final score and message!

## Files

- `personal_quiz_app.py` — the full quiz program
- `Teacher_Guide.md` — how to use this with students
- `Student_Guide.md` — instructions written for kids
- `assets/` — supporting files (currently empty, reserved for future question banks)

## Example Run (Real Captured Transcript)

This is a real transcript captured by running the script with `subprocess` and simulated input — all 5 answers correct:

```
Welcome, space traveler! What is your name? Hi Maya! Let's play a quick quiz. Answer each question and see how you do!

Q1. What color do you get when you mix blue and yellow? Correct! 🎉
Q2. How many legs does a spider have? Correct! 🎉
Q3. What planet do we live on? Correct! 🎉
Q4. What is your favorite hobby? Nice! reading sounds like a lot of fun, Maya!
Q5. What is 3 + 4? Correct! 🎉

=== Maya's Quiz Results ===
You scored 5 out of 5!
Amazing job, Maya! You're a quiz superstar! 🏆
```

And here is a real transcript with mostly wrong answers, showing the lower-score feedback path:

```
Welcome, space traveler! What is your name? Hi Leo! Let's play a quick quiz. Answer each question and see how you do!

Q1. What color do you get when you mix blue and yellow? Oops! The answer was green.
Q2. How many legs does a spider have? Oops! The answer was 8.
Q3. What planet do we live on? Oops! The answer was Earth.
Q4. What is your favorite hobby? Nice! soccer sounds like a lot of fun, Leo!
Q5. What is 3 + 4? Oops! The answer was 7.

=== Leo's Quiz Results ===
You scored 1 out of 5!
Nice try, Leo! Keep practicing and you'll do even better!
```

Both runs completed with no errors or tracebacks (verified via `subprocess.run(..., capture_output=True)` with `returncode == 0`).

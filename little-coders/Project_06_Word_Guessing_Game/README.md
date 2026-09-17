# Project 06: Word Guessing Game 🔤🔍

## What This Project Is

The computer secretly picks a random word from a list of 10 kid-friendly words. The player has 5 attempts to guess the WHOLE word. If they get it, they win! If they run out of attempts, the computer reveals the secret word.

## Why Whole-Word Guessing (Not Letter-by-Letter)

We chose whole-word guessing instead of a letter-by-letter game (like Hangman) because it is simpler to build using only what's taught through Lesson 6 (variables, input, if/else, while loops, lists, and the `random` module), and it keeps the game short, fast-paced, and fun for ages 6-11 without needing extra tools like tracking which letters have been guessed already.

## What It Uses (from Lessons 1-6)

- A Python **list** of secret words (`word_list`)
- The **`random`** module (`random.choice()`) to pick a secret word
- Variables to track attempts and whether the player has won
- `input()` to collect guesses
- `if`/`else` to check guesses and give feedback
- A `while` loop for limited attempts, and an outer `while` loop to play again

## How to Run It

1. Open `word_guessing_game.py` in Thonny or Repl.it.
2. Press Run (or F5).
3. Type your guess for the secret word each time you're asked.
4. See if you win within 5 attempts!
5. Choose to play again or stop.

## Files

- `word_guessing_game.py` — the full game program
- `Teacher_Guide.md` — how to use this with students
- `Student_Guide.md` — instructions written for kids
- `assets/word_list_notes.txt` — the word list used in the game, for reference

## Example Run (Real Captured Transcript)

Real transcript of a WIN, captured with `subprocess` and simulated input (guessing every word in the list until the right one hits):

```
=== Welcome to the Word Guessing Game! ===
I'm thinking of a secret word from outer space and beyond...
Here's a hint: it has 6 or more letters, and it's a word you know!

You have 5 attempts to guess the secret word.
Guess the secret word: 🎉 You got it! The word was 'python'. You win!

Do you want to play again? (yes/no) 
Thanks for playing the Word Guessing Game! See you next time! 👋
```

Real transcript of a LOSS (secret word was randomly "dragon", which wasn't in the first 5 guesses tried):

```
=== Welcome to the Word Guessing Game! ===
I'm thinking of a secret word from outer space and beyond...
Here's a hint: it has 6 or more letters, and it's a word you know!

You have 5 attempts to guess the secret word.
Guess the secret word: Not quite! You have 4 attempt(s) left.
Guess the secret word: Not quite! You have 3 attempt(s) left.
Guess the secret word: Not quite! You have 2 attempt(s) left.
Guess the secret word: Not quite! You have 1 attempt(s) left.
Guess the secret word: 😢 Out of attempts! The secret word was 'dragon'.

Do you want to play again? (yes/no) 
Thanks for playing the Word Guessing Game! See you next time! 👋
```

Both runs completed with `returncode == 0` and no tracebacks or unhandled exceptions.

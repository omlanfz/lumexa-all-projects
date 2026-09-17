"""
Word Guessing Game
--------------------
The computer secretly picks a word from a list. The player tries to guess
the WHOLE word within a limited number of attempts. We picked whole-word
guessing (instead of letter-by-letter, like Hangman) because it is simpler
to build with what's taught in Lessons 1-6 (variables, input, if/else,
while loops, lists, and the random module) and it keeps the game short and
fun for young coders, while still using a real word list and randomness.

Ties back to Lesson 6: uses the `random` module and a Python list.
"""

import random

# A list of at least 8-10 kid-friendly secret words.
word_list = [
    "python", "rocket", "planet", "galaxy", "wizard",
    "dragon", "castle", "puzzle", "rainbow", "volcano"
]

print("=== Welcome to the Word Guessing Game! ===")
print("I'm thinking of a secret word from outer space and beyond...")
print(f"Here's a hint: it has {len(word_list[0])} or more letters, and it's a word you know!")
print()

play_again = "yes"

while play_again == "yes":
    secret_word = random.choice(word_list)
    max_attempts = 5
    attempts_used = 0
    has_won = False

    print(f"You have {max_attempts} attempts to guess the secret word.")

    while attempts_used < max_attempts and not has_won:
        guess = input("Guess the secret word: ")
        attempts_used = attempts_used + 1

        if guess.lower() == secret_word:
            has_won = True
            print(f"🎉 You got it! The word was '{secret_word}'. You win!")
        else:
            remaining = max_attempts - attempts_used
            if remaining > 0:
                print(f"Not quite! You have {remaining} attempt(s) left.")
            else:
                print(f"😢 Out of attempts! The secret word was '{secret_word}'.")

    print()
    play_again = input("Do you want to play again? (yes/no) ")
    print()

print("Thanks for playing the Word Guessing Game! See you next time! 👋")

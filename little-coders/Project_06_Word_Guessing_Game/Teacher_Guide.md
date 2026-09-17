# Teacher Guide: Project 06 — Word Guessing Game

## Purpose
This capstone project reinforces lists and the `random` module from Lesson 6, combined with loops (Lesson 5) and if/else (Lesson 4). It's a great final portfolio piece to show off before Lesson 8's open-ended final project.

## Suggested Use
- Play the game as a class first, having a few volunteers try to guess out loud.
- Point out how `random.choice(word_list)` means nobody — not even the teacher — knows the secret word in advance.
- Have students add 3-5 of their own words to `word_list`.
- Discuss why whole-word guessing was chosen over letter-by-letter guessing (see README for the explanation) — this is a good discussion point about designing games to match your current skill level.

## What to Look For
- Do students understand that `random.choice()` picks unpredictably from the list each time?
- Can students explain why `max_attempts` limits the number of tries?
- Do they notice `.lower()` is used so capitalization doesn't cause a false "wrong" answer?

## Common Issues Students May Hit
- Forgetting `import random` if they rewrite the program from scratch.
- Adding a new word to the list without a comma, breaking the list syntax.
- Confusing the inner `while` loop (attempts within one round) with the outer `while` loop (whether to play another round).

## Extension Ideas
- Add a hint system that reveals the first letter after 2 failed attempts.
- Track and print the player's win/loss record across multiple rounds using a counter variable.
- Let advanced students try converting it into a letter-by-letter Hangman-style game as a bonus stretch project.

# Teacher Guide — Project 02: Interactive Quiz Game

## Purpose
This project models everything students need for Lesson 6 (conditionals) and Lesson 8 (final game with a Score variable), packaged as a complete, real quiz game.

## How to Use in Class
1. Play it live with the whole class answering out loud, or have students play individually with headphones/quiet voices.
2. Open Quizzy's code and show the `ask and wait` + `answer` + `if/else` + `=` pattern as ONE reusable "quiz question" recipe that repeats 5 times.
3. Point out that typed answers must match exactly what's expected (case doesn't matter, but spelling does) — a great real discussion about how computers compare text literally, connecting back to Lesson 1's "computers don't guess" idea.
4. Show how the final results message is built by joining "You got " + the Score variable + " out of 5! 🏆" using the `join` block.

## Key Teaching Moments
- **Variables as memory:** `Score` is a little box that remembers a number across the whole quiz — connect to the "variable is a little box" analogy.
- **Reusable pattern:** Each question follows the same shape (ask → compare → celebrate or comfort), which is a great intro to noticing patterns in code.
- **Kindness in feedback:** Even wrong answers get an encouraging, informative message — discuss why that matters for a good learning game.

## Discussion Questions
- "What would happen if a player typed 'Red' with a capital R? Try it and see!"
- "Why do we reset Score to 0 at the very start of the green flag script?"
- "How does Quizzy know which costume to show after each answer?"

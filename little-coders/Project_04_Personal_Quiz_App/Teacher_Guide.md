# Teacher Guide: Project 04 — Personal Quiz App

## Purpose
This project is a capstone application of Lessons 1-7. Students should be able to read, run, and eventually modify this quiz independently, using variables, input, f-strings, if/elif/else, and simple counting.

## Suggested Use
- Have students first run the finished `personal_quiz_app.py` as-is to understand the flow.
- Then have them modify at least 2 questions to topics of their own choosing (their favorite subject, book, or hobby).
- Encourage students to add a 6th question independently, following the same pattern (`answerN`, `if`/`else`, `score = score + 1`).

## What to Look For
- Does the student's added question follow the same variable-naming pattern?
- Do they remember to update the "out of 5" text if they add more questions (e.g., "out of 6")?
- Do they test both a correct and incorrect answer path?

## Common Issues Students May Hit
- Comparing a number-like answer without quotes (e.g., `if answer2 == 8` instead of `"8"`).
- Forgetting to increase `score` inside the `if` block for a new question.
- Copy-paste indentation issues when duplicating a question block.

## Extension Ideas
- Have students add a timer-like message ("Speed round!") without an actual timer, just for fun narrative flavor.
- Have students personalize the final tiered messages further.
- Advanced students can try converting the quiz to use a list of questions/answers and a loop (preview of more advanced coding, optional and not required).

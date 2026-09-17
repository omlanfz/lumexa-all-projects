# Project 02: Interactive Quiz Game — "Quizzy's Space Quiz"

A complete, playable Scratch (.sb3) project built for Lumexa Little Coders Path, Course 10 (Scratch Adventures).

## Files
- `project.sb3` — the real, playable Scratch project.
- `assets/` — generated SVG costume art and WAV sound tones.
- `source/build_project02.py` — the Python build script (uses `_sb3lib/sb3_builder.py`).
- `Teacher_Guide.md`, `Student_Guide.md`, `Project_Overview.md` — supporting materials.

## What Happens
Quizzy the Robot asks 5 real quiz questions (space, Scratch basics, shapes, coding vocabulary, and math), one at a time, using "ask and wait." Each answer is checked with an `=` operator inside an if/else block. Correct answers celebrate with a happy costume, a cheerful sound, and +1 to a Score variable; incorrect answers show an encouraging message with the right answer and a gentle "oops" sound. After the 5th question, a results screen plays a fanfare and announces "You got X out of 5! 🏆"

## How It Was Built
Run `python3 source/build_project02.py` from the `source/` folder. It builds one sprite (Quizzy) with a Score variable, 5 ask-and-wait questions each wrapped in `control_if_else` comparing `answer` to the correct text, and a final results message built with `operators_join`.

# Project Overview — Interactive Quiz Game

## Theme
A friendly robot quiz host that asks real questions, checks answers, and keeps score — the Course 10 portfolio piece that shows off variables, sensing, and conditionals working together.

## The 5 Quiz Questions
1. "What color is the planet Mars usually called?" → red
2. "In Scratch, what do we call the characters we code?" → sprite
3. "What shape has 3 sides?" → triangle
4. "What do we call a block that repeats code many times?" → loop
5. "What is 2 + 2?" → 4

## Sprite
| Sprite | Role | Costumes | Sounds |
|---|---|---|---|
| Quizzy | Quiz host robot | quizzy-idle, quizzy-happy, quizzy-oops | correct, wrong, fanfare |

## Variables
- `Score` — starts at 0, +1 for every correct answer, shown on stage.
- `QuestionNum` — tracks which question number is currently being asked.

## Learning Concepts Demonstrated
- `ask and wait` + `answer` reporter (sensing)
- `operators_equals` comparing the player's answer to the correct text
- `control_if_else` branching for correct vs. incorrect feedback
- `data_setvariableto` / `data_changevariableby` for score tracking
- `operators_join` to build a dynamic results message combining text and a variable

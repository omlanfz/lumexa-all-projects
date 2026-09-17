# Lumexa Brick Breaker

A classic breakout-style brick breaker built with Python and Pygame for the Lumexa Game Creator Path, Course 02: Python Arcade Games (Project 06).

## Description

Bounce the ball off your paddle to smash a full grid of bricks. Normal bricks shatter in one hit; tough silver bricks take two hits and crack visibly after the first. Clear two levels of increasing difficulty, keep your three lives, and rack up the highest score you can.

## Learning Objectives

- Implementing proper rect-based (AABB) ball physics with wall, paddle, and brick collision.
- Reflecting a ball's angle realistically based on where it strikes the paddle.
- Determining which side of a rectangle was struck using overlap-depth comparison, for correct brick-bounce direction.
- Building a full brick grid with two brick types (normal vs. tough/multi-hit).
- Managing a lives system, score, level progression, and a complete state machine.

## Technologies

- Python 3.10+
- Pygame 2.6.1

## Gameplay / Core Mechanics

- **Paddle:** Move left/right to keep the ball in play.
- **Ball physics:** Rect-based collision against walls, the paddle, and bricks. Hitting the paddle off-center changes the ball's angle (hit it near an edge for a sharper angle). The ball gradually speeds up with every brick hit, capped at a maximum speed.
- **Brick types:** Normal bricks (one hit) and tough bricks (two hits, visibly cracks after the first hit and turns silver) — early rows are tough, increasing on level 2.
- **Lives:** Start with 3 lives; losing the ball below the paddle costs a life and re-serves a fresh ball; losing your last life ends the game.
- **Score:** Points awarded per brick destroyed, more for tough bricks.
- **Levels:** Two brick layouts of increasing difficulty (more tough bricks in level 2).
- **Full state flow:** Menu → Serve (ball waits on paddle) → Playing → Level Clear (next level or restart) / Game Over → restart.

## Project Structure

```
06-brick-breaker-clone/
├── README.md
├── requirements.txt
└── src/
    ├── main.py       - entry point, sets up Pygame and runs the loop
    ├── settings.py   - shared constants (paddle/ball/brick sizing, colors)
    ├── paddle.py      - Paddle sprite
    ├── ball.py        - Ball sprite: physics, wall/paddle/brick reflection
    ├── bricks.py      - Brick sprite (normal + tough) and grid construction
    ├── audio.py       - SoundManager (safe, optional sound/music)
    ├── ui.py          - HUD and menu/level-clear/game-over screen drawing
    ├── game.py        - Game class: the full state machine
    └── sounds/        - optional .wav/.ogg files (game runs silently without them)
```

## Requirements

- Python 3.10 or later
- pygame (pinned in `requirements.txt`)

## Installation

```
pip install -r requirements.txt
```

## How to Run

From the project's root folder:

```
python src/main.py
```

## Controls

| Key | Action |
|---|---|
| Arrow keys / A-D | Move the paddle |
| SPACE | Launch the ball (while serving) / advance to next level (after clearing a level) |
| ENTER or SPACE (menu) | Start the game |
| R (game over, or level clear on the final level) | Restart |
| ESC | Return to menu (in-game) or quit (menu/level-clear/game-over) |

## How the Game Works

`Game` in `game.py` implements a state machine (`MENU`, `SERVE`, `PLAYING`, `LEVEL_CLEAR`, `GAME_OVER`). During `SERVE`, the ball rests on the paddle until SPACE launches it. `Ball.update()` moves the ball and reflects it off the screen's walls; `Game.update()` handles paddle and brick collisions specifically — `bounce_off_paddle()` angles the reflection based on strike position, and `bounce_off_brick()` compares overlap depth on each axis to decide whether to reflect horizontal or vertical velocity, so the ball bounces correctly whether it hits a brick's side, top, or bottom. Each brick tracks its own `health`; tough bricks require two hits (`take_hit()` returns `True` only once health reaches zero) and visually crack after the first hit. Losing the ball below the paddle costs a life and restarts the serve; clearing all bricks advances the level; running out of lives ends the game.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt`.
- **`ModuleNotFoundError: No module named 'settings'`** — run with `python src/main.py` from the project root.
- **Ball seems to pass through a brick corner without bouncing correctly** — this is expected occasionally at very high speeds/corners in simple AABB physics; the game resolves the single closest colliding brick per frame to keep behavior predictable.
- **No sound** — expected and safe if `src/sounds/` is empty; the game works identically, just silently.

## Extension Ideas

- Add falling power-ups (multi-ball, wider paddle, slow-motion) dropped by destroyed bricks.
- Add a third level with a brick pattern requiring bank shots off the side walls.
- Add a screen-shake or particle burst effect when a tough brick is finally destroyed.
- Add a local high-score file (see Project 05's JSON save-file pattern for a ready-made technique).

# Lumexa Maze Runner Timer

A maze-navigation game with a countdown timer, built with Python and Pygame for the Lumexa Game Creator Path, Course 02: Python Arcade Games (Project 05).

## Description

Guide your explorer through a tile-based maze from start to the glowing green exit before the clock runs out. Watch out for patrolling hazard drones — touching one sends you back to the start and costs you precious seconds. Beat your own best time, saved locally between sessions, across two increasingly difficult levels.

## Learning Objectives

- Representing a level as a text-based grid and converting it into `pygame.Rect` wall geometry.
- Implementing axis-separated rect collision so movement along walls feels smooth.
- Building a countdown timer using delta time (`dt`) and displaying it live in a HUD.
- Implementing a simple patrolling hazard with bounce-based AI.
- Persisting data (best completion times) to a local JSON file safely.
- Managing multiple levels and a full win/lose/restart state machine.

## Technologies

- Python 3.10+
- Pygame 2.6.1
- Python's built-in `json` module for local score persistence

## Gameplay / Core Mechanics

- **Objective:** Navigate from the start tile to the exit tile before time runs out.
- **Movement:** Smooth 8-directional movement with wall collision resolved per axis, so sliding along a wall never gets you stuck.
- **Timer:** A visible countdown (per level) shown in the HUD, turning red under 10 seconds.
- **Hazard:** At least one patrolling hazard sprite per level that bounces off walls; contact resets your position to the start and subtracts time from your countdown.
- **Scoring / best time:** Your completion time for each level is compared against a locally saved best time (`src/best_times.json`), created and updated automatically.
- **Levels:** Two maze layouts of increasing difficulty and size/time-limit tuning.
- **Full state flow:** Menu → Playing → Win (advance to next level or replay) / Timeout (retry) → restart.

## Project Structure

```
05-maze-runner-timer/
├── README.md
├── requirements.txt
└── src/
    ├── main.py       - entry point, sets up Pygame and runs the loop
    ├── settings.py   - shared constants (tile size, colors, time limits)
    ├── mazes.py       - text-based maze level layouts
    ├── maze.py        - Maze class: parses layouts into wall rects, draws the maze
    ├── player.py      - Player sprite with axis-separated wall collision
    ├── hazard.py      - Hazard sprite: patrols and bounces off walls
    ├── scores.py      - local best-time persistence (JSON file, safely guarded)
    ├── audio.py       - SoundManager (safe, optional sound/music)
    ├── ui.py          - HUD and menu/win/timeout screen drawing
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
| Arrow keys / WASD | Move through the maze |
| ENTER or SPACE (menu) | Start the game |
| SPACE (after a win, not the final level) | Advance to the next level |
| R (win on final level, or timeout) | Restart |
| ESC | Return to menu (in-game) or quit (menu/win/timeout) |

## How the Game Works

`Game` in `game.py` implements a state machine (`MENU`, `PLAYING`, `WIN`, `TIMEOUT`). Each level's text layout in `mazes.py` is parsed by `Maze` into a list of wall `pygame.Rect`s, a start position, an exit rect, and hazard spawn points. `Player` moves using axis-separated collision resolution against `maze.collides_with_wall()`. `Hazard` patrols in a straight line and reverses direction using the same wall-collision check. Every frame the countdown timer (`self.time_left`) decreases by `dt`; reaching the exit rect triggers a win and a best-time save via `scores.py` (a small JSON file, loaded and written defensively so a missing or corrupt file never crashes the game); the timer reaching zero triggers the timeout screen.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt`.
- **`ModuleNotFoundError: No module named 'settings'`** — run with `python src/main.py`, not from inside another directory.
- **Best time never seems to save** — check that the `src/` folder is writable; if it's read-only (e.g., some sandboxed environments), `scores.py` silently skips saving rather than crashing, and best time will show as `--`.
- **No sound** — expected and safe if `src/sounds/` is empty; the game works identically, just silently.
- **Player looks stuck on a wall corner** — this is expected with axis-separated collision at tight diagonals; release one direction key and the player will slide free.

## Extension Ideas

- Add a third, larger maze level with two hazards.
- Add a minimap or "fog of war" that only reveals nearby tiles.
- Add a key-and-locked-door mechanic requiring the player to find a key before the exit unlocks.
- Track and display a full leaderboard of the last 5 completion times per level, not just the single best.

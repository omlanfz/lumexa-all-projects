# Orbit Drop

A physics-based puzzle game built in Python and Pygame, for the Lumexa Game Creator Path, Course 03: Advanced Game Design (Project 08).

## Description

Aim and launch a ball using real gravity, velocity, and collision-response physics to reach a glowing goal zone on each of six hand-designed levels of increasing difficulty. Drag from the ball to aim, release to fire, and watch it bounce realistically off walls and obstacles until it settles — or misses, and you try again.

## Learning Objectives

- Implement real, simple 2D physics from first principles: gravity as constant acceleration, velocity integration over time (`dt`), and circle-vs-rectangle collision response with restitution (bounciness).
- Apply data-driven level design (Course 03, Lesson 02): every level is a plain dictionary of obstacle rectangles, a launcher position, and a goal, loaded by one generic `Level` loader.
- Practice a full menu → level-select → playing → win → next-level progression flow using an explicit finite state machine.
- Design levels following a "teach, test, twist" difficulty curve (Lesson 02).

## Technologies

- Python 3.10+
- Pygame 2.6.1

## Gameplay / Core Mechanics

- **Real physics**: constant gravity accelerates the ball; velocity is integrated every frame; friction gradually settles the ball; collisions with walls and boxes reflect velocity along the collision normal, scaled by a restitution (bounciness) constant.
- **Aim-and-launch controls**: click near the ball and drag away from your intended direction (like a slingshot), then release to launch — the drag distance and direction set the launch power and angle, visualized with a live aim line.
- **6 distinct hand-designed levels** of increasing difficulty, loaded from a clean data structure in `level_data.py` (open shots → single obstacles → narrow gaps → ledge landings → multi-barrier "twist" levels).
- **Level-select screen** with progressive unlocking: completing a level unlocks the next one.
- **Win condition per level**: the ball must come to rest (or pass through) the goal zone.
- **Reset/retry**: press `R` at any time during play to instantly restart the current level, or use "Replay Level" from the win screen.

## Project Structure

```
08-physics-puzzle-game/
├── README.md
├── requirements.txt
└── src/
    ├── main.py            # Game class, main loop, input handling, state wiring
    ├── settings.py        # Constants: gravity, restitution, friction, colors
    ├── level_data.py       # The 6 levels as plain data dictionaries
    ├── level.py            # Level loader: turns level_data into real objects
    ├── ui.py               # Buttons, title/level-select/win screens, HUD
    ├── game_state.py       # GameStateMachine: TITLE/LEVEL_SELECT/PLAYING/WIN/...
    └── entities/
        ├── ball.py         # Ball physics: gravity, velocity, collision response
        └── obstacle.py     # StaticBox obstacles and the Goal zone
```

## Requirements

- Python 3.10 or newer
- pip

## Installation

```bash
cd 08-physics-puzzle-game
pip install -r requirements.txt
```

## How to Run

```bash
cd src
python main.py
```

## Controls

| Input | Action |
|---|---|
| Click + drag from the ball, then release | Aim and launch the ball (slingshot-style) |
| R | Restart/retry the current level |
| Esc | Return to the level-select screen |
| Mouse click | Menu / level-select / win-screen buttons |

## How the Game Works

Each level is described as plain data: a launcher position, a list of obstacle rectangles, and a goal circle. The `Level` loader converts this into real `Ball`, `StaticBox`, and `Goal` objects. Every frame, the ball's velocity is affected by constant gravity and integrated into its position; if it overlaps a wall or box, `resolve_circle_rect_collision()` pushes it out and reflects its velocity along the collision surface's normal, scaled down by a restitution constant so the bounce loses energy realistically. Once the ball is moving slowly enough and touching the floor (or overlaps the goal at any point mid-flight), the level resolves: reaching the goal zone marks the level won, unlocks the next level, and shows a win overlay with options to continue, replay, or return to the level-select screen.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt` first.
- **The ball won't launch** — make sure you click *near* the ball itself (within a small radius) before dragging; clicking elsewhere on the screen won't start an aim.
- **The ball never settles / bounces forever in a corner** — press `R` to instantly retry the level; extremely narrow gaps can occasionally trap a ball with residual velocity, which is a great real playtesting observation per Lesson 06.
- **Game window doesn't appear on a headless Linux server** — run with a virtual framebuffer, e.g. `xvfb-run python main.py`.

## Extension Ideas

- Add a second ball type with different mass/bounciness for new puzzle mechanics.
- Add a star-rating system based on number of attempts per level.
- Add moving obstacles (platforms that slide back and forth) for extra challenge.
- Persist `unlocked_count` to a save file so progress carries over between sessions.

# Nova Drift

A polished, original side-scrolling platformer built in Python and Pygame — the capstone portfolio project for the Lumexa Game Creator Path, Course 03: Advanced Game Design (Project 09).

## Description

Guide a small star-drifting explorer across three increasingly challenging space-station levels: jump between solid and moving platforms, dodge spike hazards and patrolling enemies, collect glowing star shards, and reach the goal flag on each level. Checkpoints save your progress mid-level, a health and lives system governs failure, and a full title-screen-to-victory-screen experience ties it all together.

## Learning Objectives

This project intentionally combines every lesson of Course 03:

- **Lesson 01 (Game Design Fundamentals):** a tight core loop (run/jump → collect/avoid → reach checkpoint) with a deliberately tuned difficulty curve and clear positive (shards, checkpoints) and negative (hazards, enemies) feedback loops.
- **Lesson 02 (Level Design):** three hand-designed, data-driven levels (`level_data.py`) following a "teach, test, twist" progression.
- **Lesson 03 (OOP Architecture):** a clean `Entity`-based class hierarchy, composition (`JuiceManager` owned by `Game`), and an explicit `GameStateMachine`.
- **Lesson 05 (UI/UX):** a polished title screen, HUD (health bar, lives, shard count, level name), pause menu, and win/lose overlays.
- **Lesson 06 (Playtesting):** balance values (jump height, gravity, enemy speed) tuned through iterative testing.
- **Lesson 07 (Performance):** an object-pooled `JuiceManager` for floating-text popups instead of constant allocation.
- **Lesson 08 (Final Polish):** screen shake, floating damage/collect popups, invincibility-frame flicker feedback, and defensive (try/except-guarded) sound loading so the game runs cleanly with no audio files present.

## Technologies

- Python 3.10+
- Pygame 2.6.1

## Gameplay / Core Mechanics

- **Side-scrolling platformer movement**: run, jump, and fall with real gravity and a smoothly-following camera.
- **Moving platforms**: several platforms oscillate along an axis and carry the player along while standing on them.
- **Collectibles**: animated star shards add to your score; collecting one shows an instant "+1" popup.
- **Health system**: 3 HP per life, invincibility frames after taking damage (with a visible flicker), and 3 lives total.
- **Checkpoints**: touching a checkpoint flag updates your respawn point; losing all HP respawns you there instead of restarting the whole level.
- **3 hand-designed levels** of increasing difficulty, each with a distinct name, layout, and enemy/hazard density.
- **Full state machine**: Title → Playing → Paused / Level Complete / Game Over → next level or restart → Game Complete.
- **Clear win screen** after completing all three levels, showing your total shard count.

## Project Structure

```
09-published-portfolio-game/
├── README.md
├── DESIGN_DOCUMENT.md   # Core design thinking: loop, goal, challenge, feedback, etc.
├── requirements.txt
└── src/
    ├── main.py            # Game class, main loop, camera, collision resolution
    ├── settings.py        # Constants: physics values, colors, sizes
    ├── level_data.py       # The 3 levels as plain data dictionaries
    ├── level.py            # Level loader: data -> real game objects
    ├── game_state.py       # GameStateMachine: TITLE/PLAYING/PAUSED/...
    ├── ui.py               # Buttons, title/HUD/pause/win/lose screens
    ├── juice.py            # Screen shake + pooled floating-text popups
    └── entities/
        ├── entity.py       # Base Entity class
        ├── player.py       # Player physics, health, invincibility
        ├── platform.py     # Platform and MovingPlatform
        ├── hazard.py       # Spike hazards
        ├── enemy.py        # Patrolling enemy
        ├── collectible.py  # Star shard pickups
        └── checkpoint.py   # Checkpoint flags and the level Goal
```

## Requirements

- Python 3.10 or newer
- pip

## Installation

```bash
cd 09-published-portfolio-game
pip install -r requirements.txt
```

## How to Run

```bash
cd src
python main.py
```

## Controls

| Key | Action |
|---|---|
| Left/Right or A/D | Move |
| Space or Up/W | Jump |
| P | Pause / Resume |
| Esc (while paused) | Quit to title screen |
| Mouse click | Menu / overlay buttons |

## How the Game Works

Each level is described as plain data in `level_data.py` (platform rectangles, moving-platform definitions, hazard rectangles, enemy patrol data, collectible positions, checkpoints, and a goal position); `level.py` loads this data into real entity objects, exactly following the data-driven pattern from Lesson 02. Every frame, the player's velocity is affected by gravity and integrated into position, with axis-separated collision resolution against all platforms (static and moving); standing on a moving platform carries the player along by that platform's own per-frame delta. Touching a hazard or enemy calls `Player.take_damage()`, which encapsulates invincibility frames and triggers "juice" feedback (screen shake, a floating "-1 HP" popup). Reaching 0 HP costs a life and respawns the player at their last checkpoint; running out of lives triggers the Game Over state. Reaching the goal flag on the final level triggers the Game Complete victory screen.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt` first.
- **No sound plays** — this is expected: no audio files are bundled, and sound loading is wrapped in `try/except` so the game runs silently and normally without them. Add real `.wav` files under an `assets/` folder next to `main.py` (`collect.wav`, `hurt.wav`, `win.wav`) to enable sound.
- **The game window doesn't appear on a headless Linux server** — run with a virtual framebuffer, e.g. `xvfb-run python main.py`.
- **Falling into a gap doesn't seem to do anything at first** — falling far enough below the level counts as taking damage, which then respawns you at your last checkpoint; there is a short grace distance before this triggers.

## Extension Ideas

- Add a save/continue system that persists unlocked levels and total shard count between sessions.
- Add a double-jump or wall-jump ability unlocked partway through the game.
- Add a boss encounter at the end of Level 3.
- Add real sound effects and background music (the sound-loading code already supports this — just add the files).

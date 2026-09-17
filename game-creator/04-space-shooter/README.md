# Lumexa Space Shooter

A vertical arcade space shooter built with Python and Pygame, created for the Lumexa Game Creator Path, Course 02: Python Arcade Games (Project 04).

## Description

Pilot the Lumexa Voyager against waves of increasingly aggressive alien fighters. Move, dodge, and shoot your way through escalating waves, manage your lives and health, and chase a new high score every run. Full menu, pause, and game-over flow included.

## Learning Objectives

- Applying `pygame.sprite.Sprite` and `pygame.sprite.Group` to organize a real game.
- Implementing rect-based collision detection (`spritecollide`, `groupcollide`).
- Building rule-based enemy AI with patrol movement and timed shooting.
- Structuring a complete game state machine (menu, playing, paused, game over).
- Adding optional, crash-proof sound effects and music via `pygame.mixer`.
- Organizing a Pygame project into clean, professional modules.

## Technologies

- Python 3.10+
- Pygame 2.6.1

## Gameplay / Core Mechanics

- **Movement:** 8-directional flight within the screen bounds.
- **Shooting:** Fire with a cooldown so shots feel controlled, not spammy.
- **Enemy waves:** Enemies patrol left-right, bounce off screen edges, and fire back on individual timers. Every wave increases enemy speed, fire rate, and enemy count, and enemies from wave 4 onward take two hits to destroy.
- **Collisions:** Bullets destroy enemies (with a procedurally-drawn explosion effect and score), enemy bullets and ramming enemies damage the player.
- **Lives and invulnerability:** 3 lives; after taking a hit that costs a life, you get a brief flickering invulnerability window before damage can apply again.
- **Difficulty scaling:** Enemy speed, fire rate, and formation size increase with each wave number.
- **Full state machine:** Menu → Playing → Paused → Game Over → restart back to Menu/Playing, with a persisted best-score-of-the-session display.

## Project Structure

```
04-space-shooter/
├── README.md
├── requirements.txt
└── src/
    ├── main.py       - entry point, sets up Pygame and runs the loop
    ├── settings.py   - all shared constants
    ├── player.py     - Player sprite class
    ├── enemy.py      - Enemy sprite class + wave spawning
    ├── bullet.py     - shared Bullet sprite (player and enemy)
    ├── effects.py    - Explosion effect and Starfield background
    ├── audio.py      - SoundManager (safe, optional sound/music)
    ├── ui.py         - HUD and menu/game-over screen drawing
    ├── game.py       - Game class: the full state machine
    └── sounds/       - optional .wav/.ogg files (game runs silently without them)
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
| Arrow keys / WASD | Move the ship |
| SPACE | Fire (hold or tap; limited by cooldown) |
| P | Pause / resume |
| M | Mute / unmute audio |
| ENTER or SPACE (menu) | Start the game |
| R (game over) | Restart |
| ESC | Return to menu (in-game) or quit (menu/game over) |

## How the Game Works

The game is driven by a `Game` class in `game.py` implementing a state machine (`GameState.MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`). `start_new_game()` resets every piece of mutable state (player, sprite groups, score, lives, wave number) so restarting never leaves stale data behind. Each frame: input is handled per-state, `update()` advances physics/AI/collisions only while `PLAYING`, and `draw()` renders the correct screen. Enemies use a simple timer-based "AI" (patrol and shoot-on-timer) that gets tougher every wave. All sound loading in `audio.py` is wrapped in `try`/`except`, so the game runs perfectly with no sound files present in `src/sounds/`.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt`.
- **`ModuleNotFoundError: No module named 'settings'`** — make sure you're running `python src/main.py` (the script adds its own folder to the import path automatically).
- **No sound at all** — this is expected and safe if `src/sounds/` is empty or missing; add `.wav`/`.ogg` files named `shoot.wav`, `explosion.wav`, `hit.wav`, `powerup.wav`, `gameover.wav`, `theme.ogg` to hear audio.
- **Window doesn't open / immediately closes** — run from a terminal (not by double-clicking) so you can read any error output.

## Extension Ideas

- Add a boss enemy every 5th wave with a unique bullet pattern.
- Add power-ups (shield, rapid-fire, extra life) as collectible sprites.
- Add a persistent high-score file saved to disk (see Project 05's local save-file pattern for a ready-made technique).
- Add screen shake or particle bursts on explosions for extra juice.

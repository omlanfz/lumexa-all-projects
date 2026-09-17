# Starlight Relic

A top-down RPG-lite adventure game built in Python and Pygame, for the Lumexa Game Creator Path, Course 03: Advanced Game Design (Project 07).

## Description

Explore the village of Lumexa Hollow, speak with two NPCs whose dialogue advances a branching storyline, collect the Ancient Key, use it to convince Guard Talos to let you pass, and retrieve the stolen Starlight Relic to save the village and reach a clear ending.

## Learning Objectives

- Apply data-driven level/world design (Course 03, Lesson 02) to build a game world from a grid of characters.
- Apply clean OOP game architecture (Course 03, Lesson 03): an `Entity` base class, `Player`/`NPC`/`Item` subclasses, and composition (`Inventory` owned by `Player`).
- Build a branching dialogue system driven by data (a dialogue tree dictionary), not hard-coded conditionals.
- Track story/quest progress with an explicit finite state machine (`QuestManager` / `QuestStage`) instead of scattered boolean flags.
- Build a UI/HUD overlay showing live quest objectives and inventory contents.

## Technologies

- Python 3.10+
- Pygame 2.6.1

## Gameplay / Core Mechanics

- **Top-down movement** around a tile-based village map (WASD / Arrow keys).
- **Two NPC dialogue interactions**: Elder Mira (gives the quest, offers optional lore branch) and Guard Talos (blocks the way until you show him the key).
- **Inventory mechanic**: pick up the Ancient Key and the Starlight Relic; both are tracked and shown live in the HUD.
- **A simple quest with a clear completion condition**: Accept quest → find key → convince guard → retrieve relic → quest complete.
- **Story-progress state**: `QuestManager` (in `src/quest.py`) is an explicit state machine (`NOT_STARTED → ACTIVE → KEY_FOUND → GUARD_PASSED → COMPLETE`) that also drives what each NPC says when you talk to them again.
- **Save / checkpoint system**: press `F5` at any time during exploration to save your progress (quest stage, inventory, position, collected items) to `starlight_relic_save.json`; press `F9` to load it back.
- **Win / ending state**: retrieving the Starlight Relic triggers a dedicated win screen with a "Play Again" option.

## Project Structure

```
07-rpg-adventure-storyline/
├── README.md
├── requirements.txt
└── src/
    ├── main.py            # Game class, main loop, wires everything together
    ├── settings.py        # Constants: screen size, colors, speeds, fonts
    ├── map_data.py         # The world map as a data-driven grid of characters
    ├── world.py            # Loads map_data into real walls/tiles/NPCs/items
    ├── quest.py            # QuestManager: the story-progress state machine
    ├── inventory.py        # Inventory component (composition, owned by Player)
    ├── dialogue.py         # DialogueBox UI: renders branching conversations
    ├── ui.py               # HUD, Button, title screen, win screen
    ├── game_state.py       # GameStateMachine: TITLE/EXPLORING/DIALOGUE/WIN
    └── entities/
        ├── entity.py       # Base Entity class
        ├── player.py       # Player entity (movement, facing, inventory)
        ├── npc.py          # NPC base class + Elder and Guard subclasses
        └── item.py         # Item base class + AncientKey and StarlightRelic
```

## Requirements

- Python 3.10 or newer
- pip

## Installation

```bash
cd 07-rpg-adventure-storyline
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
| WASD / Arrow Keys | Move the player |
| E / Enter / Space | Interact with a nearby NPC (opens dialogue) |
| Up / Down (in dialogue) | Select a dialogue option |
| Enter / Space / E (in dialogue) | Confirm selected dialogue option |
| 1-9 (in dialogue) | Jump directly to a numbered dialogue option |
| F5 | Save game (checkpoint) |
| F9 | Load game (from checkpoint) |
| Mouse click | Click title/win screen buttons |

## How the Game Works

The player explores a single village map loaded from a plain-text grid (`map_data.py`). Walking into an NPC's interaction zone and pressing `E` opens a `DialogueBox` built from that NPC's branching dialogue tree; choosing an option can trigger a story effect (like starting the quest) and/or move to another dialogue node. Walking over the Ancient Key adds it to your inventory and advances the quest stage. Guard Talos physically blocks his tile until the quest manager confirms you have the key; once you show it to him in dialogue, he steps aside. Reaching and touching the Starlight Relic while the quest is at the correct stage collects it, completes the quest, and transitions the game to the win screen.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install -r requirements.txt` inside the project folder first.
- **Game window doesn't appear / crashes immediately on Linux** — ensure you have a display available (SDL requires a windowing system); on headless servers, run with a virtual framebuffer (e.g., `xvfb-run python main.py`).
- **Save/load does nothing** — check the console output printed after pressing F5/F9; a missing or corrupted `starlight_relic_save.json` will print a message rather than crashing.
- **Guard Talos won't let me pass** — make sure you picked up the Ancient Key (check the HUD inventory line) and talk to him again; the dialogue automatically updates once you have it.

## Extension Ideas

- Add a second quest chain with its own NPC and item.
- Add a simple day/night color-tint cycle using a timer.
- Add sound effects for pickups and dialogue advancement (guarded in `try/except` so the game still runs without audio files).
- Expand the map with multiple connected screens/rooms instead of one single view.

# Project 01: Animated Animal Story — "Pip the Bunny's Big Adventure"

A complete, playable Scratch (.sb3) project built for Lumexa Little Coders Path, Course 10 (Scratch Adventures).

## Files
- `project.sb3` — the real, playable Scratch project. Open it at scratch.mit.edu ("Load from your computer") or in the offline Scratch editor.
- `assets/` — the generated SVG costume art and WAV sound tones used inside the project (source files, also embedded in the .sb3).
- `source/build_project01.py` — the Python build script (uses `_sb3lib/sb3_builder.py`) that generates `project.sb3` from scratch. Re-run it any time to rebuild the file.
- `Teacher_Guide.md`, `Student_Guide.md`, `Project_Overview.md` — supporting materials.

## What Happens in the Story
Pip the bunny hops out of the meadow, meets a friendly (but equally river-shy) fox, and together they reach a wide river. A wise old turtle appears and carries them across on its shell. The story ends back home, with Pip and two new friends. Three scenes (Meadow → River → Home) are linked with real Scratch broadcasts.

## How It Was Built
Run `python3 source/build_project01.py` from the `source/` folder (it locates `_sb3lib` automatically). The script uses the `Project`/`Sprite` DSL to build 3 sprites (Pip, Fox, Turtle) with 2 costumes each for hop/step animation, a 3-backdrop Stage, sound cues, and broadcast-driven scene changes, then zips it into `project.sb3`.

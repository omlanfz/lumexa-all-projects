# Project 03: Creative Music Maker — "Lumexa Sound Studio"

A complete, playable Scratch (.sb3) project built for Lumexa Little Coders Path, Course 10 (Scratch Adventures).

## Files
- `project.sb3` — the real, playable Scratch project.
- `assets/` — generated SVG costume art and WAV sound tones (each instrument's real tone/sequence).
- `source/build_project03.py` — the Python build script (uses `_sb3lib/sb3_builder.py`).
- `Teacher_Guide.md`, `Student_Guide.md`, `Project_Overview.md` — supporting materials.

## What Happens
Five instrument sprites (Drum, Bell, Xylo, Bass, Chime) sit on a music studio backdrop. Click any of them, or press its number key (1–5), and it plays its own tone or short rhythmic note sequence while pulsing bigger and flashing to a bright "pulse" costume, then settling back down. Clicking around freely lets a child "compose" simple music, visually and audibly.

## How It Was Built
Run `python3 source/build_project03.py` from the `source/` folder. Each instrument sprite gets 2 costumes (idle/pulse), 1–3 note sounds at different pitches, and two identical trigger scripts — one for `when this sprite clicked` and one for `when key [N] pressed` — both calling the same play-and-pulse sequence.

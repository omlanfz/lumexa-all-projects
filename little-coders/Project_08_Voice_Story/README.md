# Project 08 — Voice-Activated Scratch Story: "Luna and the Whispering Woods"

A complete, branching interactive story starring Luna the fox, with a real choice point that changes which of two full scenes and endings you experience.


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## What's real and working right now
- A full story told through the `Narrator` sprite's say-bubbles, with a companion sprite `Luna` who visually reacts (changes costume and position) as the story unfolds.
- A real branching choice point: after the opening scene, you choose LEFT (toward the river) or RIGHT (toward the old oak tree).
- Two full, different scenes and two different, complete endings depending on your choice.
- Sound effects (a chime at scene changes, unique ending sounds).
- Keyboard stand-in for your "spoken word": press **1** to say "LEFT", press **2** to say "RIGHT".

## How to play
1. Open `project.sb3` in the Scratch editor.
2. Click the green flag and read the story as it appears in speech bubbles.
3. When asked, press **1** for LEFT or **2** for RIGHT.
4. Watch the rest of the story and its ending play out. Try the other choice on a second playthrough!

## Files in this folder
- `project.sb3` — the real, playable branching story (game-logic layer).
- `Teacher_Guide.md`, `Student_Guide.md`
- `AI_Training_Guide.md` — how to train a REAL spoken-word recognizer.
- `Scratch_Integration_Guide.md` — exactly which block to swap for the real AI block.
- `assets/` — generated costume/sound source files.

## The AI upgrade (next step, not included yet)
This story is ready for real spoken voice commands ("left"/"right") trained by a student on ML4Kids' Sounds project type. See `AI_Training_Guide.md` and `Scratch_Integration_Guide.md`.

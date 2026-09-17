# Project 07 — AI Rock-Paper-Scissors

A complete, playable Rock-Paper-Scissors game built in Scratch: you play against a computer opponent that picks randomly, with live score-keeping and a win/lose/tie sound + message for every round.


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## What's real and working right now
- A `Referee` sprite that runs the whole game: computer's random choice, the win/lose/tie decision logic, and the `Score` variable.
- Three clickable sprites — **Rock**, **Paper**, **Scissors** — you can click directly, OR use the keyboard.
- Keyboard stand-in for your "gesture": press **1** = Rock, **2** = Paper, **3** = Scissors.
- Sounds and spoken (say-bubble) reactions for winning, losing, and tying.
- A `Score` variable shown on stage that goes up every time you win a round.

## How to play
1. Open `project.sb3` in the Scratch editor (scratch.mit.edu → File → Load from your computer, or the Scratch desktop app).
2. Click the green flag.
3. Press 1, 2, or 3 (or click the Rock/Paper/Scissors sprite) to make your choice.
4. Watch the computer's random pick and the round result appear.

## Files in this folder
- `project.sb3` — the real, playable Scratch game (game-logic layer).
- `Teacher_Guide.md` — how to run this as a classroom activity.
- `Student_Guide.md` — kid-friendly play + explore instructions.
- `AI_Training_Guide.md` — how to train a REAL hand-gesture recognition model.
- `Scratch_Integration_Guide.md` — exactly which block to swap for the real AI block.
- `assets/` — the generated costume/sound source files used to build `project.sb3`.

## The AI upgrade (next step, not included yet)
This game is ready for a real webcam-based "rock/paper/scissors" gesture recognizer trained by a student on Teachable Machine or ML4Kids. See `AI_Training_Guide.md` to train it, and `Scratch_Integration_Guide.md` to wire it into this exact project.

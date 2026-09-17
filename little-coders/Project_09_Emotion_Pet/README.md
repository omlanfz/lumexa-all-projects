# Project 09 — Emotion-Recognition Virtual Pet

A complete, cute virtual pet that reacts to different moods with its own costume, sound, and a live `Happiness` meter — ready for a real facial-expression AI upgrade.


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## What's real and working right now
- A `Pet` sprite with FOUR costumes: neutral, happy, sad, and surprised.
- A `Happiness` variable (0-100) shown on stage, that changes when a mood is triggered, clamps at 0 and 100, and slowly drifts down over time (so the pet needs ongoing care/interaction, just like a real virtual pet).
- Unique sounds and a spoken reaction message for every mood.
- A special "MAX HAPPINESS" celebration sound and message when Happiness reaches 100.
- Keyboard stand-in for facial-expression detection: press **H** = Happy, **S** = Sad, **W** = Surprised/Wow.

## How to play
1. Open `project.sb3` in the Scratch editor.
2. Click the green flag.
3. Press **H**, **S**, or **W** to show the pet different moods and watch Happiness change.
4. Try to get Happiness all the way to 100!

## Files in this folder
- `project.sb3` — the real, playable virtual pet (game-logic layer).
- `Teacher_Guide.md`, `Student_Guide.md`
- `AI_Training_Guide.md` — how to train a REAL facial-expression recognition model.
- `Scratch_Integration_Guide.md` — exactly which block to swap for the real AI block.
- `assets/` — generated costume/sound source files.

## The AI upgrade (next step, not included yet)
This pet is ready for real facial-expression recognition trained by a student on Teachable Machine or ML4Kids (image-based, using faces instead of hand gestures/objects). See `AI_Training_Guide.md` and `Scratch_Integration_Guide.md`.

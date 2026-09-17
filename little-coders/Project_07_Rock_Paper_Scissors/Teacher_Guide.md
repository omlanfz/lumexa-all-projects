# Teacher Guide — Project 07: AI Rock-Paper-Scissors


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## Purpose
This is the Lesson 4 main project and a Course 12 portfolio piece. It gives students a complete, testable game BEFORE adding real AI, so they learn to separate "build the logic" from "add the AI" — a real software engineering practice.

## Classroom use
1. Open `project.sb3` with the class (projector) and play a few rounds together.
2. Have students open the code and identify: the random computer-choice block, the win/lose/tie if/else-if chain, and the Score variable.
3. Let students play individually or in pairs, then remix one small element (sound, message, backdrop).
4. Optionally (advanced/extension groups), walk through `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to add real webcam gesture recognition.

## Assessment ideas
- Can the student explain, in their own words, why Rock beats Scissors but loses to Paper, by tracing the code?
- Can the student correctly identify which single event block (keypress 1/2/3) would be replaced by a real AI block?
- Did the student's remix work without breaking the game (test it live)?

## Common issues
- If the Scratch editor shows "missing extension" — it won't, because this project uses only standard Scratch blocks; no extensions are required to open and play it.
- If students expect the webcam to already work — remind them this file is the GAME LOGIC layer only; the AI layer is a separate, later step they do themselves on a live website.

# Teacher Guide — Project 08: Voice-Activated Scratch Story


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## Purpose
This is the Lesson 6 main project and a Course 12 portfolio piece. It shows students how a branching narrative is really just broadcasts moving between scenes — a direct extension of the broadcast skills from Course 11 — with the added twist that the choice-trigger will later come from real recognized speech.

## Classroom use
1. Project `project.sb3` for the whole class; play through both branches (LEFT then RIGHT) so everyone sees both endings.
2. Have students open the Narrator sprite's code and trace each broadcast: `SaidLeft`/`SaidRight` → branch scene → `EndingBrave`/`EndingHappy`.
3. Students play individually, then write one new line of dialogue for their favorite scene.
4. Optional extension: read through `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to add real voice recognition.

## Assessment ideas
- Can the student name every broadcast used in the story and where it leads?
- Can the student correctly explain that pressing 1/2 stands in for saying "left"/"right" out loud?
- Did they successfully find and describe both endings?

## Common issues
- Story speech bubbles may need a moment to read — the built-in `wait` blocks pace this, but slower readers may want to pause with the Scratch stop/pause controls between exchanges.
- If a student presses both keys quickly, only the first choice's broadcast chain will run to its ending — this is expected branching behavior, not a bug.

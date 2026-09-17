# Teacher Guide — Project 09: Emotion-Recognition Virtual Pet


> **Important honesty note:** `project.sb3` in this folder is a REAL, COMPLETE, and FULLY PLAYABLE Scratch project — every block, sprite, sound, and animation in it actually works today, with no placeholders. It does **not** yet contain real AI recognition (no live webcam gesture/face detection or live microphone word recognition is built into the file), because a real trained model has to be created live, by a real student, on Teachable Machine or ML4Kids — that step cannot be faked or pre-baked into a downloadable file. Right now the "AI signal" is stood in for by a simple keyboard press or sprite click, described exactly below. Follow `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to train a real model and wire its real generated block into this project.


## Purpose
This is the Lesson 7 main project and a Course 12 portfolio piece. It reuses the Course-long variable/meter idea (like Happiness) and shows students that the SAME image-recognition training process from Lesson 2 (Teachable Machine) can be applied to a brand-new kind of example: human faces and expressions, not just objects.

## Classroom use
1. Project `project.sb3`; demo pressing H, S, and W and show the Happiness meter and costume changing live.
2. Have students open the Pet sprite's code and find: the `sensing_keypressed` blocks, where Happiness changes, and the clamp-to-100/0 logic.
3. Let students play, then design (on paper) a new mood and its trigger.
4. Optional extension: read `AI_Training_Guide.md` and `Scratch_Integration_Guide.md` to add real facial-expression recognition with a webcam.

## Assessment ideas
- Can the student explain what happens to Happiness over time if the pet is never interacted with, and why that design choice was made?
- Can the student correctly map each key (H/S/W) to its mood and describe what a real AI upgrade would replace?
- Can the student find the special "MAX HAPPINESS" celebration logic in the code?

## Common issues
- If Happiness seems to decrease "on its own," this is the intended background-drift script (a `forever` loop with a `wait`), not a bug — it teaches that virtual pets, like real ones, need ongoing care.
- Facial expressions in the real AI upgrade can be affected by lighting just like hand gestures — remind students of that lesson from Project 07 if they do the upgrade.

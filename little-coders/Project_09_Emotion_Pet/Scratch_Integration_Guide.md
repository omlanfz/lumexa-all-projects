# Scratch Integration Guide — Project 09: Emotion-Recognition Virtual Pet

This guide explains EXACTLY which stand-in blocks in `project.sb3` to replace with your real trained facial-expression AI blocks from `AI_Training_Guide.md`.

## What to replace
In the **Pet** sprite, `project.sb3` currently has THREE separate hat scripts that look like this:
- `when key [h] pressed` → switch costume to "happy" → play sound "happy" → change `Happiness` by 15 → (clamp) → say "Yay! I feel HAPPY!" → (max-happiness check)
- `when key [s] pressed` → switch costume to "sad" → play sound "sad" → change `Happiness` by -15 → (clamp) → say "Oh no, I feel SAD..." → (max-happiness check)
- `when key [w] pressed` → switch costume to "surprised" → play sound "wow" → change `Happiness` by 5 → (clamp) → say "Whoa! I'm SURPRISED!" → (max-happiness check)

These three keypress events are the exact stand-in for real facial-expression recognition.

## Step-by-step replacement
1. Open your ML4Kids project (trained in `AI_Training_Guide.md`), go to **Make**, and click **Scratch 3**. Your custom "recognise image" reporter block will now be at the bottom of the blocks palette.
2. Use File → Load from your computer to import this project's `project.sb3` into this ML4Kids-powered Scratch editor (this brings in the Pet sprite with all its scripts).
3. Go to the **Pet** sprite's code.
4. Keep every block AFTER the "switch costume" step exactly as it is in each of the three scripts (the sound, the Happiness change, the clamp checks, the say block, and the max-happiness check) — none of that logic needs to change.
5. Delete (or disconnect) the three `when key pressed` hat blocks described above.
6. In their place, build one new script: `when green flag clicked` → `forever` → `if <(recognise image) = [Happy]> then` → run the same "happy" block sequence (switch costume/play sound/change Happiness/etc.) → `else if <(recognise image) = [Sad]> then` → run the "sad" sequence → `else if <(recognise image) = [Surprised]> then` → run the "surprised" sequence. Add a `wait 1 seconds` after each detected match inside the forever loop so it doesn't repeatedly re-trigger every single frame.
7. Test: click the green flag, make a real happy/sad/surprised face at your webcam, and confirm the pet reacts correctly and the Happiness meter changes.

## Result
After this swap, the pet's costume changes, sounds, Happiness meter math, and max-happiness celebration all work exactly as before — only the trigger becomes a real recognized facial expression instead of a key press.

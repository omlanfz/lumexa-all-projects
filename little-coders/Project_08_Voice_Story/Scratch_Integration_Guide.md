# Scratch Integration Guide — Project 08: Voice-Activated Story

This guide explains EXACTLY which stand-in blocks in `project.sb3` to replace with your real trained voice-recognition blocks from `AI_Training_Guide.md`.

## What to replace
In the **Narrator** sprite, `project.sb3` currently has these two stand-in hat scripts:
- `when key [1] pressed` → broadcast `SaidLeft`
- `when key [2] pressed` → broadcast `SaidRight`

These two keypress events are the exact stand-in for real recognized speech.

## Step-by-step replacement
1. Open your ML4Kids voice project (trained in `AI_Training_Guide.md`), go to **Make**, and click **Scratch 3**. Your custom "recognise sound" reporter block will now be available at the bottom of the blocks palette.
2. Use File → Load from your computer to import this project's `project.sb3` into this ML4Kids-powered Scratch editor (this brings in the Narrator and Luna sprites with all their scripts).
3. Go to the **Narrator** sprite's code.
4. Keep the rest of the story scripts (`when I receive SaidLeft`, `when I receive SaidRight`, and both ending scripts) exactly as they are — they never need to change.
5. Delete (or disconnect) the two `when key pressed` hat blocks described above.
6. In their place, build one new script: `when green flag clicked` → `forever` → `if <(recognise sound) = [left]> then` → broadcast `SaidLeft` → `stop [this script]` `else if <(recognise sound) = [right]> then` → broadcast `SaidRight` → `stop [this script]`. Using `stop this script` after a correct match prevents the choice from firing more than once per playthrough.
7. Test: click the green flag, wait for the story to reach the choice point, and say "left" or "right" out loud into your microphone. Confirm the correct branch and ending play.

## Result
After this swap, all the actual story content, scene changes, and endings work exactly as before — only the trigger for `SaidLeft`/`SaidRight` becomes a real recognized spoken word instead of a key press.

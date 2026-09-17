# Scratch Integration Guide — Project 07: Rock-Paper-Scissors

This guide explains EXACTLY which stand-in blocks in `project.sb3` to replace with your real trained AI blocks from `AI_Training_Guide.md`.

## What to replace
In the **Referee** sprite, `project.sb3` currently has THREE separate hat scripts that look like this:
- `when key [1] pressed` → set `PlayerChoice` to "Rock" → play sound "click" → broadcast `PlayerChose`
- `when key [2] pressed` → set `PlayerChoice` to "Paper" → play sound "click" → broadcast `PlayerChose`
- `when key [3] pressed` → set `PlayerChoice` to "Scissors" → play sound "click" → broadcast `PlayerChose`

These three keypress events are the exact stand-in for your real AI gesture recognition.

## Step-by-step replacement
1. Open your ML4Kids project (the one you trained in `AI_Training_Guide.md`), go to **Make**, and click **Scratch 3**. This opens a Scratch editor with your custom AI block already available (look at the very bottom of the blocks palette, in its own colored category).
2. **Import your existing game**: in this new ML4Kids-powered Scratch editor, use File → Load from your computer and select this project's `project.sb3` to bring in the whole rock-paper-scissors game (all sprites, scripts, sounds).
3. Go to the **Referee** sprite's code.
4. Keep the game logic scripts (the `when I receive PlayerChose` script and the `when I receive ShowResult` script) exactly as they are — those never need to change.
5. Delete (or disconnect) the three `when key pressed` hat blocks described above.
6. In their place, build a NEW forever loop: `when green flag clicked` → `forever` → `if <(recognise image) = [Rock]> then` → set `PlayerChoice` to "Rock" → broadcast `PlayerChose` → `else if <(recognise image) = [Paper]> then` → set `PlayerChoice` to "Paper" → broadcast `PlayerChose` → `else if <(recognise image) = [Scissors]> then` → set `PlayerChoice` to "Scissors" → broadcast `PlayerChose`. (Use nested if/else blocks, or ML4Kids' extra "else if" block if available, to check all three labels.)
7. Add a short `wait 1 seconds` inside the forever loop after a successful match so the game doesn't fire the same recognition dozens of times per second.
8. Test: click the green flag, hold up a real Rock/Paper/Scissors gesture to your webcam, and confirm the Referee correctly detects it and plays a round.

## Result
After this swap, everything downstream (computer's random pick, win/lose/tie logic, Score, sounds) works completely unchanged — only the INPUT to `PlayerChoice` becomes a real trained AI prediction instead of a key press.

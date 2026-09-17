# AI Training Guide — Project 07: Rock-Paper-Scissors Gesture Recognition

This guide walks you through training a REAL image-recognition model that can look at your hand through a webcam and tell Rock, Paper, or Scissors apart — using either Teachable Machine or ML4Kids. Do this AFTER you've played and understood the base `project.sb3` game.

## Option A: Using Teachable Machine + ML4Kids together (recommended path)
Teachable Machine is great for training, but to get a Scratch block you need ML4Kids' "Make" feature, so the full real path uses **ML4Kids** end-to-end. (Teachable Machine is still useful in Lesson 2 for practice.)

### Step-by-step (ML4Kids)
1. Go to **machinelearningforkids.co.uk** and log in to your class account (ask your teacher if you don't have a login).
2. Click **+ Add new project**. Name it "Rock Paper Scissors AI." Choose recognition type **Images**.
3. Open the project and go to the **Train** tab.
4. Add THREE labels/buckets: `Rock`, `Paper`, `Scissors`.
5. For EACH label, click **Webcam** and record 20-30 example photos of your hand making that exact shape. Move your hand a little between photos (different angle, distance, slight rotation) so the model learns the SHAPE, not just one exact pose.
6. Make sure your hand fills a good chunk of the frame and the background is reasonably plain and consistent across all three labels (so the model learns your hand shape, not your background).
7. Go to **Learn & Test**. Click **Train new machine learning model** and wait for it to finish.
8. Test it live in the Test box: hold up Rock, Paper, and Scissors and check the model guesses correctly most of the time. If any label is weak, add more varied examples for it and retrain.

## Tips for a strong model
- Use at least 25 examples per label (more is better).
- Vary lighting, distance, and slight hand angle — don't record all examples in one exact spot.
- Keep the background reasonably consistent between labels so the model doesn't accidentally learn "background" instead of "hand shape."
- If two labels keep getting confused (e.g., Paper vs. Rock), add more contrasting examples and retrain.

## What's next
Once your model tests well (aim for consistently correct guesses across several tries per label), move on to `Scratch_Integration_Guide.md` to connect it to `project.sb3`.

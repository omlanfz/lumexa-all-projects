# AI Training Guide — Project 09: Training a Facial Expression Recognizer

This guide walks you through training a REAL image-recognition model that can look at your FACE through a webcam and tell happy, sad, and surprised expressions apart, using Teachable Machine or ML4Kids.

## Step-by-step (Teachable Machine, then bring it into ML4Kids for Scratch — OR train directly in ML4Kids)

### Using ML4Kids directly (recommended, since it produces the Scratch block)
1. Go to **machinelearningforkids.co.uk** and log in to your class account.
2. Click **+ Add new project**. Name it "Pet Emotions." Choose recognition type **Images**.
3. Open the project and go to the **Train** tab.
4. Add labels matching the pet's moods: `Happy`, `Sad`, `Surprised`.
5. For EACH label, click **Webcam** and record 20-30 example photos of YOUR real face making that expression. Move your head slightly and vary distance/angle a little between photos so the model learns the general expression pattern, not one exact frozen pose.
6. Try to keep lighting and background reasonably similar across all three labels, so the model focuses on your FACE, not the room around you.
7. Go to **Learn & Test**, click **Train new machine learning model**, and wait.
8. Test live: make a happy face, a sad face, and a surprised face in front of the webcam and check the model recognizes each one most of the time. Add more varied examples and retrain for any weak label.

## Tips for a strong model
- Really commit to each expression (big smile for Happy, real frown for Sad, wide eyes/open mouth for Surprised) — subtle, half-hearted expressions are harder for the model to learn.
- Use at least 25 examples per label, with small natural variation in angle/lighting.
- Keep the same general lighting and background between labels so the model doesn't accidentally learn the ROOM instead of the FACE.
- If Happy and Surprised get confused, add clearer, more different examples for each.

## What's next
Once your model recognizes all three expressions reliably, move on to `Scratch_Integration_Guide.md` to connect it to `project.sb3`.

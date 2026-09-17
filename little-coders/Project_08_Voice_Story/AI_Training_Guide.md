# AI Training Guide — Project 08: Training a "Left"/"Right" Voice Recognizer

This guide walks you through training a REAL sound-recognition model on ML4Kids that can hear you say "left" or "right" out loud and recognize which word you said.

## Step-by-step (ML4Kids Sounds project)
1. Go to **machinelearningforkids.co.uk** and log in to your class account.
2. Click **+ Add new project**. Name it "Story Voice Commands." Choose recognition type **Sounds**.
3. Open the project and go to the **Train** tab.
4. Add THREE labels/buckets: `left`, `right`, and `background noise`.
5. Click the microphone icon under `left` and record yourself clearly saying "left" — repeat until you have 15-20 short examples. Do the same for `right`.
6. For `background noise`, record a few clips of quiet room sound (no talking) — this helps the model tell "you said a word" apart from "silence/room noise."
7. Go to **Learn & Test**, click **Train new machine learning model**, and wait for it to finish.
8. Test live: say "left," then "right," into the microphone and check the model recognizes each one correctly most of the time. If it's confused, record more clear examples for the weaker label and retrain.

## Tips for a strong model
- Speak clearly at a normal, consistent volume — avoid whispering or shouting.
- Record in a reasonably quiet room; heavy background noise in only some clips will confuse the model.
- Say the word naturally each time, with a little natural variation, rather than the exact same recording repeated.

## What's next
Once "left" and "right" are each recognized reliably, move on to `Scratch_Integration_Guide.md` to connect your model to `project.sb3`.

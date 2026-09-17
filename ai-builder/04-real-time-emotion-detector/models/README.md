# Models Directory

Place your trained emotion classification model here as:

```
emotion_model.h5
```

## Required format

- Keras HDF5 model file (`model.save("emotion_model.h5")`).
- Input shape: `(48, 48, 1)` per sample (grayscale, 48x48 pixels), batched as `(batch_size, 48, 48, 1)`.
- Output shape: `(7,)` softmax probabilities, in this exact class order:
  1. Angry
  2. Disgust
  3. Fear
  4. Happy
  5. Neutral
  6. Sad
  7. Surprise

## How to get this file

There is **no bundled or auto-downloaded model file** in this project — you must either:

1. Train one yourself using `src/emotion_model.py --train --data-dir <path> --output models/emotion_model.h5`, pointing at a labeled dataset organized into `train/<ClassName>/*.jpg` and `validation/<ClassName>/*.jpg` folders (see the main README's Configuration section for full details and an example public dataset structure).
2. Supply your own previously-trained `.h5` file that matches the input/output shape above.

If this file is missing, the application still runs in "detection-only" mode — faces are still detected and boxed, but labeled `"Model not loaded"` instead of a predicted expression.

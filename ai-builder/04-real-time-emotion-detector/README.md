# Real-Time Emotion Detector

A Lumexa Computer Vision Track portfolio project: a live webcam application that detects faces and classifies their facial expression pattern in real time, using OpenCV for face detection and a small Convolutional Neural Network (CNN) for expression classification.

## Important Disclaimer — Please Read First

**This project classifies visible facial expression patterns. It does not measure, detect, or know a person's true internal emotions.**

A neural network trained on labeled photos learns statistical correlations between facial muscle configurations (mouth shape, eyebrow position, eye openness, etc.) and human-assigned labels like "happy" or "sad." It has no access to what a person actually feels — a person can smile while anxious, or look neutral while delighted. The "confidence score" this app displays reflects how closely the detected face's pattern resembles the model's training examples, not a certainty about reality.

This system can also be **biased and inaccurate**, especially for faces, lighting conditions, ages, and expressions underrepresented in whatever dataset trained the model. Do not use this project (or any derivative of it) to make real decisions about real people — hiring, discipline, grading, medical judgments, or anything with consequences — without qualified human review and much more rigorous, audited validation than a classroom project provides. Always disclose to anyone on camera that expression analysis is running, and never record or store footage of people without their knowledge and consent.

## Overview

The app opens your webcam, detects all visible faces every frame using OpenCV's Haar Cascade classifier, crops and preprocesses each detected face, and classifies its expression into one of seven categories using a Convolutional Neural Network: Angry, Disgust, Fear, Happy, Neutral, Sad, or Surprise. Each detected face is annotated live with a bounding box, its predicted label, and a confidence percentage.

## Learning Objectives

- Understand how face detection (Haar Cascades) and expression classification (CNN) combine into one real-time pipeline.
- Learn how to preprocess a cropped face image (grayscale, resize, normalize) to match a neural network's expected input.
- Practice structuring a real-time OpenCV application with clean separation between capture, detection, classification, and rendering.
- Practice communicating AI capabilities and limitations honestly to end users.

## Features

- Real-time webcam face detection using OpenCV Haar Cascades.
- Facial expression classification across 7 categories using a Keras CNN.
- Live bounding-box and label overlay with confidence percentages.
- Confidence thresholding: low-confidence predictions are shown as "Uncertain" rather than a falsely confident label.
- FPS counter and a visible "LIVE ANALYSIS ACTIVE" on-screen indicator.
- Included training script to train your own small demo model on your own labeled image folders.
- Clear, documented expectations for the model file so you can supply a properly trained model.

## Project Structure

```
04-real-time-emotion-detector/
├── README.md
├── requirements.txt
├── models/
│   └── (place emotion_model.h5 here -- see Configuration section)
└── src/
    ├── config.py            # centralized configuration
    ├── face_detector.py     # Haar Cascade face detection wrapper
    ├── emotion_model.py      # CNN architecture, training script, and inference wrapper
    ├── renderer.py           # drawing/annotation utilities
    └── main.py                # real-time webcam application entry point
```

## Requirements

- Python 3.9 or newer
- A webcam (for live use) — static-image testing works without one
- Libraries listed in `requirements.txt`: `opencv-python`, `tensorflow`, `numpy`

## Installation

```bash
cd projects/04-real-time-emotion-detector
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

The expected trained model file is:

```
models/emotion_model.h5
```

**Expected model shape and format:**
- A Keras model saved via `model.save("emotion_model.h5")` (HDF5 format).
- Input shape: `(48, 48, 1)` — a single 48×48 grayscale image, per sample, batched as `(batch_size, 48, 48, 1)`.
- Output shape: `(7,)` — a softmax probability distribution over these 7 classes, **in this exact order**: `["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]`.

You have two options to obtain this file:

1. **Train it yourself** using the included script `src/emotion_model.py`, which contains a `train_from_directory()` function. Point it at a folder of labeled face images structured like this (a standard Keras `image_dataset_from_directory` layout):

   ```
   dataset/
   ├── train/
   │   ├── Angry/*.jpg
   │   ├── Disgust/*.jpg
   │   ├── Fear/*.jpg
   │   ├── Happy/*.jpg
   │   ├── Neutral/*.jpg
   │   ├── Sad/*.jpg
   │   └── Surprise/*.jpg
   └── validation/
       ├── Angry/*.jpg
       ├── ... (same 7 subfolders)
   ```

   A well-known public dataset with exactly this structure of labels is FER2013 (Facial Expression Recognition 2013); you may use any dataset you have appropriate rights and consent to use, reorganized into this folder layout. Run:

   ```bash
   python src/emotion_model.py --train --data-dir path/to/dataset --epochs 30 --output models/emotion_model.h5
   ```

2. **Supply your own pre-trained `.h5` file** from a previous project, as long as it matches the input shape `(48, 48, 1)` and the 7-class output order documented above. Simply place it at `models/emotion_model.h5`.

If no model file is found at startup, `main.py` will log a clear warning and run in "detection-only" mode (faces are boxed, but labeled "Model not loaded" instead of an expression).

Other tunable settings (camera index, detection sensitivity, confidence threshold) live in `src/config.py`.

## Running

```bash
python src/main.py
```

Press `q` at any time to quit. Press `s` to save a labeled snapshot of the current frame to `snapshots/` (created automatically).

## How It Works

1. **Capture** (`main.py`): `cv2.VideoCapture(0)` reads live frames from the webcam.
2. **Detection** (`face_detector.py`): each frame is converted to grayscale and passed to OpenCV's `haarcascade_frontalface_default.xml` classifier (loaded from `cv2.data.haarcascades`), returning bounding boxes for every detected face.
3. **Preprocessing** (`emotion_model.py`): each detected face region is cropped from the original color frame, converted to grayscale, resized to 48×48, and normalized to the 0–1 range to match the model's training format.
4. **Classification** (`emotion_model.py`): the preprocessed face tensor is passed to `model.predict()`, producing a 7-value softmax probability array; the highest-probability class and its value are extracted as the predicted label and confidence.
5. **Confidence thresholding**: if the top confidence is below `config.EMOTION_CONFIDENCE_THRESHOLD` (default 0.35), the label is shown as `"Uncertain"` instead of forcing a possibly-wrong-feeling confident label.
6. **Rendering** (`renderer.py`): bounding boxes, labels, confidence percentages, an FPS counter, and a "LIVE ANALYSIS ACTIVE" indicator are drawn onto the frame, which is displayed via `cv2.imshow`.

## Common Problems

- **`Could not open camera index 0`**: another application may be using the webcam, or no webcam is present. Try changing `CAMERA_INDEX` in `src/config.py` to `1` or another index, or check for a permissions issue on your OS.
- **Model shows "Model not loaded" for every face**: confirm `models/emotion_model.h5` exists and was saved with the exact input/output shape documented in Configuration above. Check the console warning for the specific loading error.
- **`ImportError: No module named tensorflow`**: run `pip install -r requirements.txt` inside your activated virtual environment.
- **Low FPS / laggy video**: try increasing `PROCESS_EVERY_N_FRAMES` in `src/config.py` to classify expressions less frequently while still displaying every frame, or use a smaller/simpler model.
- **Haar Cascade misses faces at an angle or in poor lighting**: this is a known limitation of this fast, older detection method (see Lesson 3 of the Computer Vision Track) — improving lighting or facing the camera more directly typically helps.

## Extensions

- Swap the Haar Cascade for a more modern deep-learning-based face detector (e.g., a DNN-based face detector bundled with OpenCV) for improved accuracy across angles and lighting.
- Log expression history over a session to a CSV file with timestamps, and plot a simple trend chart afterward.
- Add multi-face tracking so each detected face keeps a consistent ID across frames instead of being re-detected independently each time.
- Build a simple Tkinter or web-based settings panel to adjust the confidence threshold live without editing `config.py`.

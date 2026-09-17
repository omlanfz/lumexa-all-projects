# Object Recognition App

A Lumexa Computer Vision Track portfolio project: a real-time and static-image object detection application built on **Ultralytics YOLOv8**, a modern, actively maintained, beginner-friendly object detection library that automatically downloads pre-trained weights on first use.

## Overview

This app detects and labels everyday objects in photos or live webcam video using a pre-trained YOLOv8n ("nano") model trained on the COCO dataset (~80 common object categories: people, vehicles, animals, furniture, electronics, and more). Detected objects are annotated with a bounding box, class label, and confidence score.

## Learning Objectives

- Understand single-pass object detection ("You Only Look Once") and how it differs from sliding-window approaches.
- Learn to load and run a pre-trained YOLOv8 model using the `ultralytics` Python package.
- Practice parsing and rendering detection results (bounding boxes, class labels, confidence scores) manually.
- Learn to apply confidence thresholds and class filters to detection output.
- Understand and communicate the limitations of a closed-vocabulary detector.

## Features

- Static image object detection (`src/detect_image.py`).
- Real-time webcam object detection with FPS counter and frame-skipping for performance (`src/detect_webcam.py`).
- Configurable confidence threshold and optional class-of-interest filtering.
- Manual bounding-box/label rendering plus Ultralytics' built-in quick-plot option.
- Snapshot saving from the live webcam view.

## Project Structure

```
05-object-recognition/
├── README.md
├── requirements.txt
└── src/
    ├── config.py          # centralized configuration
    ├── detector.py        # YOLOv8 model wrapper and detection-parsing logic
    ├── renderer.py         # bounding-box/label drawing utilities
    ├── detect_image.py     # static image detection entry point
    └── detect_webcam.py    # real-time webcam detection entry point
```

## Requirements

- Python 3.9 or newer
- Internet access on first run (Ultralytics automatically downloads `yolov8n.pt`, ~6MB, from its official release servers)
- A webcam (only required for `detect_webcam.py`)
- Libraries listed in `requirements.txt`: `ultralytics`, `opencv-python`

## Installation

```bash
cd projects/05-object-recognition
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The first time you run either script, Ultralytics will automatically download the pre-trained `yolov8n.pt` weights file (trained on the COCO dataset) to a local cache folder. No manual download, account, or API key is required.

## Configuration

All tunable settings live in `src/config.py`:

- `MODEL_NAME` — which YOLOv8 variant to load (default `"yolov8n.pt"`, the fastest/smallest; other options: `yolov8s.pt`, `yolov8m.pt`, `yolov8l.pt`, `yolov8x.pt` — larger means more accurate but slower).
- `CONFIDENCE_THRESHOLD` — minimum confidence (0.0–1.0) required to report a detection (default `0.4`).
- `CLASS_FILTER` — an optional set of class names to restrict detection output to (e.g., `{"person", "dog", "car"}`); leave as `None` to detect all ~80 COCO classes.
- `CAMERA_INDEX` — which webcam device to use for `detect_webcam.py` (default `0`).
- `PROCESS_EVERY_N_FRAMES` — how often (in frames) to run detection during live video, for performance tuning.

## Running

**Static image detection:**

```bash
python src/detect_image.py path/to/your_photo.jpg
```

Saves an annotated copy as `<original_name>_detected.png` in the same folder, and prints each detection to the console.

**Real-time webcam detection:**

```bash
python src/detect_webcam.py
```

Press `q` to quit. Press `s` to save a snapshot of the current annotated frame to `snapshots/`.

## How It Works

1. **Model loading** (`detector.py`): `YOLO("yolov8n.pt")` loads the pre-trained COCO weights (auto-downloaded on first use).
2. **Inference**: calling the model on an image (`model(image, conf=threshold)`) runs a single forward pass through the network, which simultaneously predicts candidate object locations, class probabilities, and confidence scores across the entire image in one step — this is the core "You Only Look Once" idea that makes YOLO fast enough for real-time video.
3. **Parsing results**: each `Results` object's `.boxes` attribute is iterated; for every detected box, `.xyxy` gives corner coordinates, `.conf` gives the confidence score, and `.cls` gives the class index (mapped to a human-readable name via `model.names`).
4. **Filtering**: results below `CONFIDENCE_THRESHOLD`, or not in `CLASS_FILTER` (if set), are excluded before rendering.
5. **Rendering** (`renderer.py`): bounding boxes, class labels, and confidence percentages are drawn onto the frame/image.
6. **Real-time loop** (`detect_webcam.py`): frames are captured via `cv2.VideoCapture`, and detection is optionally run only every Nth frame (`PROCESS_EVERY_N_FRAMES`) to maintain smooth FPS on modest hardware, reusing the most recent detection results on skipped frames.

## Model Limitations — Please Read

- **Closed vocabulary**: this model can only ever report the ~80 object classes it was trained on as part of the COCO dataset (common categories like person, car, dog, chair, laptop, bottle — see `model.names` for the full list by running the app). It has no concept of any object outside this list; an unfamiliar object will either go undetected or be mislabeled as the closest known class.
- **Confidence scores are not guarantees**: a reported confidence of, say, 0.87 for "dog" means the detected image region's learned visual pattern closely resembles the model's "dog" training examples — not an absolute 87% certainty that a dog is truly present. The model can be confidently wrong, especially with occlusion, unusual angles, poor lighting, or objects that resemble multiple trained classes.
- **Uneven accuracy across classes**: COCO, like most datasets, contains far more labeled examples of some categories (e.g., "person," "car") than others (e.g., "toaster," "hair drier"). Detection reliability for underrepresented classes is correspondingly weaker.
- **Not appropriate for high-stakes automated decisions**: bounding boxes and labels describe pattern-matched regions, not verified facts about the world. Do not use this project, or a derivative of it, to make safety-critical or high-stakes decisions (e.g., automated access control, autonomous vehicle control) without far more rigorous, professionally audited validation than a portfolio project provides.

## Common Problems

- **First run seems to hang**: the first execution downloads `yolov8n.pt` from the internet; a slow connection can make this take a minute. Subsequent runs use the cached file and start instantly.
- **`Could not open camera index 0`**: check that a webcam is connected and not already in use by another application; try changing `CAMERA_INDEX` in `src/config.py`.
- **`ModuleNotFoundError: No module named 'ultralytics'`**: run `pip install -r requirements.txt` inside your activated virtual environment.
- **Low FPS during webcam detection**: increase `PROCESS_EVERY_N_FRAMES` in `src/config.py`, or switch to a smaller model variant if you're already using a larger one.
- **No objects detected in an image that clearly has some**: try lowering `CONFIDENCE_THRESHOLD` in `src/config.py`, or confirm the object you expect is actually one of COCO's ~80 supported classes.

## Extensions

- Add object counting and a running summary report (e.g., "3 people, 1 dog, 2 chairs detected").
- Fine-tune YOLOv8 on a custom dataset for a specialized use case beyond COCO's classes (Ultralytics supports this directly via `model.train()`).
- Add simple object tracking across frames (e.g., using Ultralytics' built-in `model.track()` mode) so each object keeps a consistent ID over time instead of being independently re-detected every frame.
- Combine with the Real-Time Emotion Detector project: detect "person" boxes with YOLO, then run face detection + expression classification only within those regions.

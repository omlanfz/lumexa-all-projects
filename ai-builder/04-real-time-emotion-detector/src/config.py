"""
Configuration for the Lumexa Real-Time Emotion Detector.

Centralizing tunable values here means the rest of the codebase never
hardcodes magic numbers -- change behavior in exactly one place.
"""

import os

# Path to this file's directory, used to build reliable relative paths
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)


class Config:
    # --- Camera ---
    CAMERA_INDEX = 0

    # --- Face detection (Haar Cascade) ---
    FACE_SCALE_FACTOR = 1.1
    FACE_MIN_NEIGHBORS = 5
    FACE_MIN_SIZE = (60, 60)

    # --- Emotion classification model ---
    MODEL_PATH = os.path.join(_PROJECT_ROOT, "models", "emotion_model.h5")
    EMOTION_INPUT_SIZE = 48  # model expects 48x48 grayscale input
    EMOTION_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]
    EMOTION_CONFIDENCE_THRESHOLD = 0.35  # below this, label is shown as "Uncertain"

    # --- Performance ---
    PROCESS_EVERY_N_FRAMES = 1  # increase to classify less often if FPS is low

    # --- Display ---
    SHOW_FPS = True
    SHOW_LIVE_INDICATOR = True
    BOX_COLOR = (0, 255, 0)          # BGR green
    UNCERTAIN_BOX_COLOR = (0, 165, 255)  # BGR orange

    # --- Snapshots ---
    SNAPSHOT_DIR = os.path.join(_PROJECT_ROOT, "snapshots")

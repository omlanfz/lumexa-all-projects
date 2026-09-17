"""
Configuration for the Lumexa Object Recognition App.
"""

import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)


class Config:
    # --- Model ---
    # "n" = nano (fastest, smallest, recommended for real-time/laptop use).
    # Other options: yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    MODEL_NAME = "yolov8n.pt"

    # --- Detection ---
    CONFIDENCE_THRESHOLD = 0.4

    # Optional: restrict detection output to specific class names.
    # Set to None to detect all ~80 COCO classes. Example:
    # CLASS_FILTER = {"person", "dog", "car", "backpack"}
    CLASS_FILTER = None

    # --- Camera (webcam mode only) ---
    CAMERA_INDEX = 0
    PROCESS_EVERY_N_FRAMES = 2  # increase to improve FPS at the cost of detection freshness

    # --- Display ---
    BOX_COLOR = (0, 200, 0)   # BGR green
    SHOW_FPS = True

    # --- Snapshots ---
    SNAPSHOT_DIR = os.path.join(_PROJECT_ROOT, "snapshots")

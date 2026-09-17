"""
Configuration for the Lumexa Motion-Activated Security Cam.
"""

import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)


class Config:
    # --- Camera ---
    CAMERA_INDEX = 0
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480

    # --- Background subtraction (motion detection) ---
    BACKGROUND_HISTORY = 500     # number of frames used to build the background model
    VAR_THRESHOLD = 40           # sensitivity: lower = more sensitive, more false positives
    DETECT_SHADOWS = True        # exclude cast shadows from motion counting

    # --- Motion filtering ---
    MIN_MOTION_AREA = 800        # minimum contour area (pixels) to count as real motion
    DILATE_ITERATIONS = 2        # morphological cleanup of the foreground mask

    # --- Event handling ---
    COOLDOWN_SECONDS = 10        # minimum time between separate logged motion events
    CAPTURES_DIR = os.path.join(_PROJECT_ROOT, "captures")

    # --- Video clip recording ---
    RECORD_VIDEO_CLIPS = True
    CLIP_DURATION_SECONDS = 5
    CLIP_FPS = 20.0

    # --- Display ---
    BOX_COLOR = (0, 0, 255)      # BGR red for motion boxes
    SHOW_FPS = True

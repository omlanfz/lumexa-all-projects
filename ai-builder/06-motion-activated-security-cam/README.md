# Motion-Activated Security Cam

A Lumexa Computer Vision Track portfolio project: a webcam application that detects motion in a live video feed using background subtraction / frame differencing, and automatically saves timestamped snapshots and video clips when motion is detected — no machine learning model required, just classic, well-understood computer vision techniques.

## Privacy Considerations — Please Read First

Building a motion-triggered camera system carries real responsibility. Before running this project, or any derivative of it, in any real space:

- **Only monitor spaces you have the clear right to monitor.** Never point this at a space (a neighbor's property, a shared area you don't control, a public street in many jurisdictions) without confirming you're legally and ethically allowed to record it.
- **Tell the people who might be recorded.** If this runs in a shared home, classroom, or workplace, let everyone who might appear on camera know it's active, what it does (detects motion and saves snapshots/clips), and where that footage goes. A visible sign or verbal notice is good practice, not just a legal nicety.
- **Think about storage and retention.** This project saves snapshots and clips to a local folder (`captures/` by default) with no automatic deletion. Decide and document how long you'll keep this footage, who can access it, and how you'll securely delete it when it's no longer needed. Recorded video of real people is sensitive data — treat it that way.
- **This project is a learning tool, not a certified security product.** It has no professional monitoring, no tamper detection, no encrypted storage, and no vetted reliability guarantees. Do not rely on it as your only safeguard for anything genuinely safety-critical.
- **Motion detection has known limitations** (see "Common Problems" below) — lighting changes, moving shadows, pets, and camera vibration can all trigger false positives, and very slow or very small movements can be missed entirely. Never treat a "no motion detected" result as a guarantee that nothing happened.

## Overview

The app continuously reads webcam frames, compares each new frame against a running background model using OpenCV's `cv2.createBackgroundSubtractorMOG2`, and identifies regions where enough pixels have changed to indicate real motion (as opposed to sensor noise). When motion exceeding a configurable area threshold is detected, the app draws bounding boxes around the moving regions, logs a console notification with a timestamp, saves a snapshot image, and can optionally record a short video clip of the motion event.

## Learning Objectives

- Understand background subtraction and frame-differencing techniques for motion detection.
- Learn to distinguish real motion from camera sensor noise using thresholding and contour area filtering.
- Practice building an event-triggered application (as opposed to a continuously-classifying one).
- Practice saving timestamped image and video output to disk.
- Think critically about the privacy responsibilities of building camera-based software.

## Features

- Real-time motion detection using `cv2.createBackgroundSubtractorMOG2`.
- Configurable sensitivity (minimum contour area required to count as "motion").
- Bounding boxes drawn around each detected motion region.
- Automatic timestamped snapshot saving on motion events.
- Optional short video clip recording for each motion event, with a configurable pre/post buffer.
- Console log notifications for every motion event, with timestamp and detected region count.
- A visible on-screen "MONITORING ACTIVE" indicator and a "MOTION DETECTED" alert overlay.

## Project Structure

```
06-motion-activated-security-cam/
├── README.md
├── requirements.txt
└── src/
    ├── config.py           # centralized configuration
    ├── motion_detector.py  # background subtraction / motion detection logic
    ├── recorder.py         # snapshot and video clip saving utilities
    └── main.py             # real-time monitoring application entry point
```

## Requirements

- Python 3.9 or newer
- A webcam
- Libraries listed in `requirements.txt`: `opencv-python`, `numpy`

## Installation

```bash
cd projects/06-motion-activated-security-cam
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

All tunable settings live in `src/config.py`:

- `CAMERA_INDEX` — which webcam device to use (default `0`).
- `MIN_MOTION_AREA` — minimum contour area (in pixels) required to count as real motion, filtering out small noise-driven fluctuations (default `800`).
- `BACKGROUND_HISTORY` — how many frames the background subtractor uses to build its model of "the normal, unmoving scene" (default `500`).
- `VAR_THRESHOLD` — sensitivity of the MOG2 background subtractor; lower values detect subtler changes but increase false positives (default `40`).
- `CAPTURES_DIR` — where snapshots and clips are saved (default `captures/`).
- `RECORD_VIDEO_CLIPS` — whether to save a short video clip (not just a still image) for each motion event (default `True`).
- `CLIP_DURATION_SECONDS` — how many seconds to record once motion is first detected (default `5`).
- `COOLDOWN_SECONDS` — minimum time between separate logged motion events, to avoid spamming captures during one continuous motion episode (default `10`).

## Running

```bash
python src/main.py
```

Press `q` to quit. The console will print a log line and the on-screen overlay will read "MOTION DETECTED" every time motion crosses the configured threshold; snapshots and (optionally) clips are saved automatically to `captures/`.

## How It Works

1. **Background modeling** (`motion_detector.py`): `cv2.createBackgroundSubtractorMOG2(history=BACKGROUND_HISTORY, varThreshold=VAR_THRESHOLD, detectShadows=True)` builds and continuously updates a statistical model of the "normal" (unmoving) scene from recent frames.
2. **Foreground mask**: for each new frame, `subtractor.apply(frame)` returns a foreground mask — a grayscale image where pixels that differ significantly from the background model are marked bright, and static background pixels are marked dark. Detected shadow regions are marked as an intermediate gray value and explicitly excluded from motion counting to reduce false positives from moving shadows.
3. **Noise cleanup**: the raw foreground mask is thresholded and passed through morphological operations (`cv2.dilate`, `cv2.erode`) to remove small, isolated noise pixels and fill in small gaps within real moving regions.
4. **Contour detection**: `cv2.findContours` finds the outlines of connected bright regions in the cleaned-up mask; each contour's area is measured with `cv2.contourArea`.
5. **Thresholding by area**: only contours larger than `MIN_MOTION_AREA` are treated as genuine motion, filtering out tiny fluctuations from sensor noise, minor lighting flicker, or small non-motion artifacts.
6. **Event handling** (`main.py`, `recorder.py`): when qualifying motion is found (and the cooldown period has elapsed since the last event), a bounding box is drawn around each motion region, a console log line with a timestamp is printed, a snapshot is saved, and — if enabled — a short video clip covering the event is recorded.

## Common Problems

- **False positives from lighting changes**: gradual daylight changes, a light turning on/off, or reflections can all register as "motion." Try increasing `VAR_THRESHOLD` in `src/config.py`, or ensure `detectShadows=True` is active (it is, by default) so cast shadows are excluded.
- **False positives from small movements** (a curtain flutter, a pet): raise `MIN_MOTION_AREA` in `src/config.py` to require larger moving regions before counting as motion.
- **Missed slow or very small motion**: background subtraction is tuned for typical human-scale movement; very slow drifting motion can sometimes be absorbed into the background model over time. Lower `BACKGROUND_HISTORY` slightly if this is a problem in your setting.
- **`Could not open camera index 0`**: check that a webcam is connected and not already in use by another application; try a different `CAMERA_INDEX`.
- **Disk filling up over time**: this project does not automatically delete old captures. Periodically review and clean out `captures/`, or add a retention-policy script (see Extensions).

## Extensions

- Add a retention policy: automatically delete captures older than N days on startup.
- Add region-of-interest masking, so motion is only monitored within a specific part of the frame (e.g., ignoring a window where outdoor tree movement causes false positives).
- **Optional notification integration (not implemented here, by design)**: you could extend `recorder.py` to send an email or push notification when motion is detected, using a service like SMTP (Python's built-in `smtplib`) or a third-party push notification API. This project intentionally does not implement any external notification service — it only logs to the console and saves local files — so that it has zero external dependencies, no required accounts, and no risk of accidentally sharing footage with a third-party service without explicit, deliberate setup by whoever deploys it.
- Combine with the Object Recognition project: run YOLO object detection only on frames where motion was already detected, to additionally report *what* triggered the motion (e.g., "person" vs. "cat") — this two-stage approach also saves significant compute compared to running object detection on every single frame continuously.

"""
Rendering/annotation utilities for the Lumexa Real-Time Emotion Detector.

This module ONLY draws onto frames -- it has no knowledge of how
detections or classifications were computed.
"""

import cv2


class ResultRenderer:
    def __init__(self, config):
        self.config = config

    def draw(self, frame, detections, fps=None):
        """
        detections: list of dicts, each with keys:
            'box' -> (x, y, w, h)
            'label' -> str
            'confidence' -> float (0.0 - 1.0)
        """
        for detection in detections:
            x, y, w, h = detection["box"]
            label = detection["label"]
            confidence = detection["confidence"]

            color = self.config.BOX_COLOR
            if label in ("Uncertain", "Model not loaded"):
                color = self.config.UNCERTAIN_BOX_COLOR

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

            if label == "Model not loaded":
                caption = label
            else:
                caption = f"{label} ({confidence * 100:.0f}%)"

            text_y = max(20, y - 10)
            cv2.putText(frame, caption, (x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

        if self.config.SHOW_LIVE_INDICATOR:
            cv2.putText(frame, "LIVE ANALYSIS ACTIVE", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2, cv2.LINE_AA)

        if fps is not None and self.config.SHOW_FPS:
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)

        return frame

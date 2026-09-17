"""
Rendering/annotation utilities for the Lumexa Object Recognition App.
"""

import cv2


class ResultRenderer:
    def __init__(self, config):
        self.config = config

    def draw(self, frame, detections, fps=None):
        """
        detections: list of dicts with keys 'box' (x1,y1,x2,y2), 'label', 'confidence'.
        """
        for detection in detections:
            x1, y1, x2, y2 = detection["box"]
            label = detection["label"]
            confidence = detection["confidence"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), self.config.BOX_COLOR, 2)
            caption = f"{label} {confidence:.2f}"
            text_y = max(20, y1 - 8)
            cv2.putText(frame, caption, (x1, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.config.BOX_COLOR, 2, cv2.LINE_AA)

        if fps is not None and self.config.SHOW_FPS:
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)

        return frame

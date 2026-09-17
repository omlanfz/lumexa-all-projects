"""
YOLOv8 object detection wrapper for the Lumexa Object Recognition App.

Responsible ONLY for loading the model and turning raw Ultralytics
results into a simple, structured list of detections -- rendering and
capture are handled by other modules.

RESPONSIBLE USE REMINDER: this detector can only ever report the ~80
COCO classes it was trained on, and its confidence scores reflect
pattern similarity to training data, not a guarantee of ground truth.
See the project README's "Model Limitations" section.
"""

import logging

from ultralytics import YOLO

logger = logging.getLogger("object_recognition.detector")


class ObjectDetector:
    def __init__(self, config):
        self.config = config
        logger.info(f"Loading YOLO model '{config.MODEL_NAME}' "
                     f"(will auto-download on first use if not cached)...")
        self.model = YOLO(config.MODEL_NAME)
        logger.info(f"Model loaded. Recognizes {len(self.model.names)} classes.")

    @property
    def class_names(self):
        return self.model.names

    def detect(self, frame_bgr):
        """
        Runs detection on a single BGR image/frame.

        Returns a list of dicts, each with keys:
            'box'        -> (x1, y1, x2, y2) integer corner coordinates
            'label'      -> str class name
            'confidence' -> float 0.0-1.0
        """
        results = self.model(frame_bgr, conf=self.config.CONFIDENCE_THRESHOLD, verbose=False)

        detections = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                if self.config.CLASS_FILTER is not None and class_name not in self.config.CLASS_FILTER:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                confidence = float(box.conf[0])

                detections.append({
                    "box": (x1, y1, x2, y2),
                    "label": class_name,
                    "confidence": confidence,
                })

        return detections

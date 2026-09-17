"""
Lumexa Object Recognition App -- static image detection entry point.

Run: python src/detect_image.py path/to/photo.jpg

Saves an annotated copy as "<name>_detected.png" next to the input file
and prints each detection to the console.
"""

import logging
import os
import sys

import cv2

from config import Config
from detector import ObjectDetector
from renderer import ResultRenderer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("object_recognition.detect_image")


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/detect_image.py path/to/photo.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    image = cv2.imread(image_path)
    if image is None:
        logger.error(f"Could not read image file: {image_path}")
        sys.exit(1)

    config = Config()
    detector = ObjectDetector(config)
    renderer = ResultRenderer(config)

    detections = detector.detect(image)
    logger.info(f"Detected {len(detections)} object(s) in {image_path}")

    for i, detection in enumerate(detections):
        print(f"  [{i}] {detection['label']} "
              f"(confidence={detection['confidence']:.2f}) "
              f"box={detection['box']}")

    annotated = renderer.draw(image.copy(), detections)

    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_detected.png"
    cv2.imwrite(output_path, annotated)
    logger.info(f"Annotated image saved to {output_path}")

    print("\nResponsible-use reminder: this detector only recognizes ~80 COCO classes, "
          "and confidence scores reflect pattern similarity to training data, not "
          "a guarantee of what is truly present. See README.md for full details.")


if __name__ == "__main__":
    main()

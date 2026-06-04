from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image as PILImage

from src.inference.base import EmotionPredictor, PredictionResult


class YoloEmotionPredictor(EmotionPredictor):
    """Loads a YOLOv8 classification `.pt` model and performs inference.

    The predictor detects the largest face in the input image with an OpenCV Haar
    cascade, crops that face region, and sends the crop to Ultralytics YOLO for
    classification.
    """

    name = "yolov8-cls"

    def __init__(self, model_path: str | Path, labels: Sequence[str] | None = None) -> None:
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model_path = model_path.resolve()

        try:
            import cv2
        except Exception as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "OpenCV is required for face detection. Install with `pip install opencv-python-headless`."
            ) from exc

        try:
            from ultralytics import YOLO
        except Exception as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "Ultralytics is required to load the YOLOv8 classification model. "
                "Install with `pip install ultralytics`."
            ) from exc

        self._cv2 = cv2
        self._face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        if self._face_cascade.empty():
            raise RuntimeError("Failed to load Haar cascade for face detection")

        self.model = YOLO(str(self.model_path))
        self.labels = self._resolve_labels(labels)

    def _resolve_labels(self, labels: Sequence[str] | None) -> list[str]:
        if labels is not None:
            return list(labels)

        env_labels = os.getenv("CLASS_NAMES", "").strip()
        if env_labels:
            return [label.strip().lower() for label in env_labels.split(",") if label.strip()]

        model_labels = getattr(self.model, "names", None)
        if model_labels:
            ordered = self._ordered_labels(model_labels)
            if ordered:
                return ordered

        return ["angry", "happy", "surprised"]

    @staticmethod
    def _ordered_labels(names: dict[int, str] | Iterable[str]) -> list[str]:
        if isinstance(names, dict):
            return [str(names[index]).strip().lower() for index in sorted(names)]
        return [str(label).strip().lower() for label in names]

    def _detect_face_crop(self, image: PILImage.Image) -> tuple[PILImage.Image, tuple[int, int, int, int]]:
        import numpy as np

        rgb = np.asarray(image.convert("RGB"))
        gray = self._cv2.cvtColor(rgb, self._cv2.COLOR_RGB2GRAY)
        faces = self._face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
        )
        if len(faces) == 0:
            raise ValueError("No face detected in the image")

        x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
        pad_x = int(w * 0.12)
        pad_y = int(h * 0.18)
        left = max(0, x - pad_x)
        top = max(0, y - pad_y)
        right = min(rgb.shape[1], x + w + pad_x)
        bottom = min(rgb.shape[0], y + h + pad_y)

        crop = rgb[top:bottom, left:right]
        if crop.size == 0:
            raise ValueError("No face detected in the image")

        return PILImage.fromarray(crop), (left, top, right - left, bottom - top)

    def predict(self, image: PILImage.Image) -> PredictionResult:
        crop_image, _ = self._detect_face_crop(image)

        results = self.model.predict(source=crop_image, verbose=False)
        if not results:
            raise RuntimeError("YOLO classification returned no results")

        result = results[0]
        probs_obj = getattr(result, "probs", None)
        if probs_obj is None:
            raise RuntimeError("YOLO classification result did not include probabilities")

        import numpy as np

        probs = np.asarray(probs_obj.data.cpu().numpy(), dtype="float32")
        if probs.size == 0:
            raise RuntimeError("YOLO classification result was empty")

        label_names = self._ordered_labels(getattr(result, "names", None) or getattr(self.model, "names", {}))
        if label_names:
            self.labels = label_names

        if probs.shape[0] != len(self.labels):
            aligned = np.zeros(len(self.labels), dtype="float32")
            count = min(len(aligned), probs.shape[0])
            aligned[:count] = probs[:count]
            probs = aligned

        total = float(probs.sum())
        if total <= 0:
            probs = np.ones_like(probs) / len(probs)
        else:
            probs = probs / total

        probabilities = {label: float(prob) for label, prob in zip(self.labels, probs)}
        top_idx = int(np.argmax(probs))
        top_label = self.labels[top_idx]
        top_conf = float(probs[top_idx])

        return PredictionResult(
            emotion=top_label,
            confidence=top_conf,
            probabilities=probabilities,
            model_name=self.name,
            notes=f"Loaded model file: {self.model_path.name} | Face detected: yes | Cropped face: yes",
        )


ModelEmotionPredictor = YoloEmotionPredictor

from __future__ import annotations

import os
from pathlib import Path

from src.inference.base import EmotionPredictor


def load_predictor() -> EmotionPredictor:
    """Loads the YOLOv8 classification inference backend."""
    backend = os.getenv("MODEL_BACKEND", "").strip().lower()
    if backend not in {"", "model", "yolo", "yolov8"}:
        raise ValueError("MODEL_BACKEND must be empty, 'model', 'yolo', or 'yolov8'")

    model_path = os.getenv("MODEL_PATH", "best_emotion_yolo.pt")
    model_file = Path(model_path)

    from src.inference.model_predictor import YoloEmotionPredictor

    return YoloEmotionPredictor(model_file)

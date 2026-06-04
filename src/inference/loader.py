from __future__ import annotations

import os
from pathlib import Path

from src.inference.base import EmotionPredictor


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve_model_file(model_path: str) -> Path:
    raw = Path(model_path).expanduser()
    if raw.is_absolute():
        return raw

    candidates = [
        Path.cwd() / raw,
        PROJECT_ROOT / raw,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    # Prefer project-root-relative location for clearer error messages downstream.
    return PROJECT_ROOT / raw


def load_predictor() -> EmotionPredictor:
    """Loads the YOLOv8 classification inference backend."""
    backend = os.getenv("MODEL_BACKEND", "").strip().lower()
    if backend not in {"", "model", "yolo", "yolov8"}:
        raise ValueError("MODEL_BACKEND must be empty, 'model', 'yolo', or 'yolov8'")

    model_path = os.getenv("MODEL_PATH", "best_emotion_yolo.pt")
    model_file = _resolve_model_file(model_path)

    from src.inference.model_predictor import YoloEmotionPredictor

    return YoloEmotionPredictor(model_file)

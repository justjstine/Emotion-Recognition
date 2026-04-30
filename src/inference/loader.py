from __future__ import annotations

import os
from pathlib import Path

from src.inference.base import EmotionPredictor


def load_predictor() -> EmotionPredictor:
    """
    Loads the inference backend.

    Supported values:
    - MODEL_BACKEND=mock  -> returns deterministic mock predictor
    - MODEL_BACKEND=model -> loads the real .h5 model predictor

    If MODEL_BACKEND is not set, the loader will try the real model first when
    an `.h5` file is available, otherwise it falls back to mock mode.
    """
    backend = os.getenv("MODEL_BACKEND", "").strip().lower()
    model_path = os.getenv("MODEL_PATH", "emotion_model.h5")
    model_file = Path(model_path)

    if backend == "":
        backend = "model" if model_file.exists() else "mock"

    if backend == "model":
        from src.inference.model_predictor import ModelEmotionPredictor

        return ModelEmotionPredictor(model_file)

    raise ValueError("MODEL_BACKEND must be either 'mock' or 'model'")

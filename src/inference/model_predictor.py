from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence

from PIL import Image as PILImage

from src.inference.base import EmotionPredictor, PredictionResult


class ModelEmotionPredictor(EmotionPredictor):
    """Loads a Keras/TensorFlow `.h5` model and performs inference.

    Behavior:
    - Attempts to import TensorFlow lazily and raises an informative error if missing.
    - Loads the model at initialization (so it's reused across requests).
    - Preprocesses PIL images by resizing to the model input shape and normalizing to [0,1].

    Notes:
    - This class is intentionally dependency-light at import time; installing
      `tensorflow` or `tensorflow-cpu` is required to actually instantiate it.
    - Supports both grayscale (1 channel) and RGB (3 channel) inputs.
    """

    name = "model-cnn-h5"

    def __init__(self, model_path: str | Path, labels: Sequence[str] | None = None) -> None:
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model_path = model_path.resolve()

        try:
            # Import lazily so the repo can be inspected without TF installed.
            from tensorflow.keras.models import load_model
            from tensorflow.keras.layers import InputLayer
        except Exception as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "TensorFlow is required to load the .h5 model. "
                "Install with `pip install tensorflow-cpu` or `tensorflow` for GPU support."
            ) from exc

        # Custom deserialization handler for InputLayer to handle legacy model files
        class LegacyInputLayer(InputLayer):
            @classmethod
            def from_config(cls, config):
                # Remove unsupported parameters from older model versions
                batch_shape = config.pop('batch_shape', None)
                if config.get("shape") is None and batch_shape is not None:
                    config["shape"] = tuple(batch_shape[1:])
                config.pop('optional', None)
                return cls(**config)

        custom_objects = {'InputLayer': LegacyInputLayer}
        self.model = load_model(
            str(self.model_path),
            custom_objects=custom_objects,
            compile=False
            )

        try:
            import cv2
        except Exception as exc:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "OpenCV is required for face detection. Install with `pip install opencv-python`."
            ) from exc

        # Determine expected input shape (height, width)
        input_shape = getattr(self.model, "input_shape", None)
        if input_shape is None:
            raise RuntimeError("Cannot determine model input shape from loaded model")

        # input_shape is typically (None, H, W, C) or (H, W, C)
        if len(input_shape) == 4:
            _, h, w, c = input_shape
        elif len(input_shape) == 3:
            h, w, c = input_shape
        else:
            raise RuntimeError(f"Unsupported model input shape: {input_shape}")

        self.input_size = (int(w), int(h))
        self.input_channels = int(c) if c is not None else 3
        self._cv2 = cv2
        self._face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        if self._face_cascade.empty():
            raise RuntimeError("Failed to load Haar cascade for face detection")

        env_labels = os.getenv("CLASS_NAMES", "")
        if labels is not None:
            self.labels = list(labels)
        elif env_labels.strip():
            self.labels = [label.strip().lower() for label in env_labels.split(",") if label.strip()]
        else:
            # Keras folder-based training commonly uses alphabetical class order.
            self.labels = ["angry", "happy", "surprised"]

    def predict(self, image: PILImage.Image) -> PredictionResult:
        import numpy as np

        # Detect face and crop to the largest bounding box.
        rgb = np.asarray(image.convert("RGB"))
        bgr = self._cv2.cvtColor(rgb, self._cv2.COLOR_RGB2BGR)
        gray = self._cv2.cvtColor(bgr, self._cv2.COLOR_BGR2GRAY)
        faces = self._face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            raise ValueError("No face detected in the image")

        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        if self.input_channels == 1:
            crop = gray[y : y + h, x : x + w]
            image = PILImage.fromarray(crop, mode="L")
        else:
            crop = rgb[y : y + h, x : x + w]
            image = PILImage.fromarray(crop)

        # Preprocess to match the model's expected channel count.
        if self.input_channels == 1:
            img = image.convert("L").resize(self.input_size)
            arr = np.asarray(img).astype("float32") / 255.0
            arr = np.expand_dims(arr, axis=-1)
        else:
            img = image.convert("RGB").resize(self.input_size)
            arr = np.asarray(img).astype("float32") / 255.0

            if arr.shape[-1] != self.input_channels:
                if self.input_channels == 1:
                    arr = np.mean(arr, axis=-1, keepdims=True)
                else:
                    arr = arr[:, :, : self.input_channels]

        # Model expects batch dimension
        batch = np.expand_dims(arr, axis=0)

        preds = self.model.predict(batch)
        # If model returns logits, apply softmax
        if preds.ndim == 2:
            probs = preds[0]
        else:
            probs = preds.flatten()

        # Normalize to sum=1
        probs = np.asarray(probs, dtype="float32")
        if probs.sum() <= 0:
            probs = np.ones_like(probs) / len(probs)
        else:
            probs = probs / probs.sum()

        # Match length to labels; if mismatch, trim or pad with zeros
        if probs.shape[0] != len(self.labels):
            # Pad or truncate
            import math

            new = np.zeros(len(self.labels), dtype="float32")
            for i in range(min(len(new), probs.shape[0])):
                new[i] = float(probs[i])
            probs = new

        probabilities = {label: float(prob) for label, prob in zip(self.labels, probs)}
        top_idx = int(probabilities and max(range(len(self.labels)), key=lambda i: probs[i]))
        top_label = self.labels[top_idx]
        top_conf = float(probs[top_idx])

        return PredictionResult(
            emotion=top_label,
            confidence=top_conf,
            probabilities=probabilities,
            model_name=self.name,
            notes=f"Loaded model file: {self.model_path.name} | Face detected: yes",
        )

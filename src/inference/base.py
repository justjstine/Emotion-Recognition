from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Protocol

from PIL.Image import Image


@dataclass
class PredictionResult:
    emotion: str
    confidence: float
    probabilities: Dict[str, float]
    model_name: str
    inference_ms: float | None = None
    notes: str = ""

    def normalized_probabilities(self) -> Dict[str, float]:
        total = sum(self.probabilities.values())
        if total <= 0:
            return self.probabilities
        return {key: value / total for key, value in self.probabilities.items()}


class EmotionPredictor(Protocol):
    name: str

    def predict(self, image: Image) -> PredictionResult:
        ...

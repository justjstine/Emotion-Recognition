from __future__ import annotations

import pandas as pd
import streamlit as st

from src.inference.base import PredictionResult


EMOJI_BY_LABEL = {
    "happy": "😄",
    "angry": "😠",
    "surprised": "😲",
}


def render_prediction_card(result: PredictionResult) -> None:
    label = result.emotion.lower().strip()
    emoji = EMOJI_BY_LABEL.get(label, "🙂")
    confidence_pct = result.confidence * 100.0

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-chip">Prediction</div>
            <div class="result-emotion">{emoji} {label.title()}</div>
            <div class="result-confidence">Confidence: {confidence_pct:.1f}%</div>
            <div class="result-meta">Model: {result.model_name}</div>
            <div class="result-meta">Latency: {result.inference_ms:.1f} ms</div>
            <div class="result-note">{result.notes}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_bars(result: PredictionResult) -> None:
    probs = result.normalized_probabilities()

    frame = pd.DataFrame(
        {
            "emotion": [key.title() for key in probs.keys()],
            "confidence": [value for value in probs.values()],
        }
    ).sort_values("confidence", ascending=False)

    st.markdown("#### Confidence by class")
    st.bar_chart(frame, x="emotion", y="confidence", color="#1f7a8c")

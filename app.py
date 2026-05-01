import time

import streamlit as st

from src.inference.loader import load_predictor
from src.ui.theme import apply_theme
from src.utils.image_io import load_image_from_buffer


st.set_page_config(
    page_title="Emotion Recognition",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()
# CSS moved to src/ui/theme.py -> apply_theme()


def emotion_style(emotion: str) -> tuple[str, str]:
    mapping = {
        "happy": ("var(--happy)", "😄"),
        "angry": ("var(--angry)", "😠"),
        "surprised": ("var(--surprised)", "😲"),
    }
    return mapping.get(emotion.lower(), ("var(--accent)", "🙂"))


def render_result_card(result) -> None:
    color, emoji = emotion_style(result.emotion)
    if result.confidence >= 0.8:
        confidence_label = "✅ High confidence"
    elif result.confidence >= 0.6:
        confidence_label = "⚠ Moderate confidence"
    else:
        confidence_label = "❗ Low confidence"
    st.markdown(
        f"""
        <div class="result-panel" style="background: {color}1a; border: 1px solid {color}55;">
            <div class="result-title">Prediction</div>
            <div style="display:flex; align-items:center; gap: 6px;">
                <div class="result-emoji">{emoji}</div>
                <div class="result-main" style="color:{color}">{result.emotion.title()}</div>
            </div>
            <div class="result-confidence">Confidence: {result.confidence * 100:.1f}%</div>
            <div class="result-note">{confidence_label}</div>
            <div class="result-note">✔ Face detected clearly</div>
            <div class="result-note">💡 Try exaggerating your expression for better results.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_bars(probabilities: dict[str, float]) -> None:
    for label, value in probabilities.items():
        color, _ = emotion_style(label)
        st.markdown(
            f"""
            <div style="margin: 8px 0 6px 0;">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-weight:600;">{label.title()}</span>
                    <span style="color: var(--muted);">{value * 100:.1f}%</span>
                </div>
                <div style="background:#e2e8f0; border-radius:999px; height:10px;">
                    <div style="width:{value * 100:.1f}%; background:{color}; height:10px; border-radius:999px;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown('<div class="app-shell">', unsafe_allow_html=True)
st.markdown('<div class="title">Emotion Recognition</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Detect emotions instantly from a selfie or a photo.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="instruction">Look at the camera, show a clear emotion, and keep your face centered.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Input")
    input_source = st.radio("Source", options=["Webcam", "Image Upload"], horizontal=False)
    st.markdown("### Options")
    show_probabilities = st.toggle("Show confidence bars", value=True)
    with st.expander("Advanced", expanded=False):
        predictor = load_predictor()
        st.caption(f"Backend: {predictor.name}")
        model_path = getattr(predictor, "model_path", None)
        if model_path is not None:
            st.caption(f"Model file: {model_path}")
        model_labels = getattr(predictor, "labels", None)
        if model_labels is not None:
            st.caption(f"Class order: {', '.join(model_labels)}")

if "predictor" not in locals():
    predictor = load_predictor()

left_col, right_col = st.columns([1.4, 1], gap="large")

image_file = None
image = None
with left_col:
    if input_source == "Image Upload":
        image_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False,
        )
        st.markdown(
            '<div class="upload-hint" style="text-align:center;">JPG, PNG, or WEBP. Try a close-up face photo.</div>',
            unsafe_allow_html=True,
        )
        if image_file is not None:
            image = load_image_from_buffer(image_file)
            st.markdown('<div style="margin-top:7px;"></div>', unsafe_allow_html=True)
            img_left, img_center, img_right = st.columns([1, 1.2, 3.2])
            with img_center:
                st.image(image, caption="Uploaded Image", width=330)
    else:
        image_file = st.camera_input("Take Photo")
    if image_file is None:
        st.markdown(
            """
            <div class="result-panel" style="background: var(--panel); border: 1px solid #e2e8f0;">
                <div class="result-title">Awaiting input</div>
                <div class="result-note">Capture a photo or upload an image to see the prediction.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

if image_file is not None and image is None:
    image = load_image_from_buffer(image_file)

with right_col:
    if image_file is not None:
        try:
            with st.spinner("Analyzing emotion..."):
                started = time.perf_counter()
                result = predictor.predict(image)
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                result.inference_ms = elapsed_ms

            render_result_card(result)
            if show_probabilities:
                render_probability_bars(result.probabilities)

        except ValueError as exc:
            if str(exc).strip().lower() == "no face detected in the image":
                st.warning("No face detected. Please try another image or recapture from webcam.")
            else:
                st.error(
                    "We could not process this image. Please try another image or recapture from webcam."
                )
                st.exception(exc)
        except Exception as exc:
            st.error("We could not process this image. Please try another image or recapture from webcam.")
            st.exception(exc)

st.markdown("</div>", unsafe_allow_html=True)

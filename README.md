# Emotion Recognition Streamlit App

## Overview

A simple Streamlit app for 3-class emotion recognition (happy, angry, surprised).
The app now loads a YOLOv8 classification model and runs inference on a cropped face region.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How It Works

- Upload an image or use the webcam input.
- The app predicts a label and confidence.
- Class confidence bars visualize all scores.

## Model Notes

- Default model file: `best_emotion_yolo.pt`.
- Face detection uses OpenCV Haar Cascade before classification.
- Update `src/inference/model_predictor.py` if you change labels, crop behavior, or model handling.
- Use `src/inference/loader.py` to control how the model is loaded.

## Notebook

Training workflow and experiments are in `Emotion_Recognition_CNN.ipynb`.

## Project Structure

```text
.
├── app.py
├── best_emotion_yolo.pt
├── Emotion_Recognition_CNN.ipynb
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── src/
  ├── components/
  │   └── prediction_card.py
  ├── inference/
  │   ├── base.py
  │   ├── loader.py
  │   └── model_predictor.py
  ├── ui/
  │   └── theme.py
  └── utils/
    └── image_io.py
```


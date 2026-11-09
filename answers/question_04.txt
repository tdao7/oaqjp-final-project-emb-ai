"""Analyze text emotions using the Watson NLP EmotionPredict service."""

import os

import requests

SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
SERVICE_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Create the null-valued result expected for HTTP 400 responses."""
    return {**{emotion: None for emotion in EMOTION_NAMES}, "dominant_emotion": None}


def _offline_example(text_to_analyze):
    """Return illustrative, non-AI output when MOCK mode is explicitly enabled.

    This demonstration is useful only for offline UI previews. It does not
    query or reproduce the IBM Watson service and must never be presented as
    a genuine service prediction.
    """
    text = text_to_analyze.lower()
    cues = {
        "anger": ("angry", "mad", "furious"),
        "disgust": ("disgust", "gross", "repulsive"),
        "fear": ("afraid", "scared", "frightened", "fear"),
        "joy": ("happy", "glad", "delighted", "joy"),
        "sadness": ("sad", "unhappy", "heartbroken"),
    }
    match = next(
        (name for name, words in cues.items() if any(word in text for word in words)),
        "joy",
    )
    emotions = {name: (0.88 if name == match else 0.03) for name in EMOTION_NAMES}
    return {**emotions, "dominant_emotion": match}


def emotion_detector(text_to_analyze):
    """Return the scores of five emotions and the dominant emotion.

    An HTTP 400 response (e.g. empty/invalid input) returns a dictionary
    containing None for all scores and for ``dominant_emotion``. Network
    errors and malformed service responses are surfaced to the caller.
    """
    if not isinstance(text_to_analyze, str):
        raise TypeError("text_to_analyze must be a string")
    if not text_to_analyze.strip():
        return _empty_result()

    if os.getenv("EMOTION_DETECTION_MOCK") == "1":
        return _offline_example(text_to_analyze)

    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(
        SERVICE_URL, json=payload, headers=SERVICE_HEADERS, timeout=15
    )
    if response.status_code == 400:
        return _empty_result()
    response.raise_for_status()

    emotions = response.json()["emotionPredictions"][0]["emotion"]
    scores = {name: float(emotions[name]) for name in EMOTION_NAMES}
    dominant_emotion = max(scores, key=scores.get)
    return {**scores, "dominant_emotion": dominant_emotion}

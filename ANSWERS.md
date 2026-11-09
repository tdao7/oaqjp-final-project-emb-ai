# Assignment answers: 16 fields

**Retake update:** The public fork at `https://github.com/tdao7/oaqjp-final-project-emb-ai` exists (and Questions 1 & 6 were awarded full marks). The corrected files in this ZIP must be pushed before their public URLs show the fix. The current GitHub integration returned HTTP 403 for writes; run `bash apply_fixes_tdao7.sh` from your local machine after Git authentication.

**Verification performed:** 7 existing unit tests and 2 retake checks passed locally. IBM Watson was not reachable here, and Flask/Pylint were not installed. Browser screenshots under `evidence/` remain **offline previews**, not deployment evidence; run `bash run_in_ibm_lab.sh` inside IBM Lab to obtain actual output and screenshots.

## Question 1 (URL)

Verified public repository URL:
https://github.com/tdao7/oaqjp-final-project-emb-ai/blob/main/README.md

STATUS: 1/1 in grading. Keep this URL unchanged.

---

## Question 2 (TEXT)

```python
"""Task 2 initial emotion_detector implementation using Watson NLP."""

import requests


def emotion_detector(text_to_analyze):
    """Return the initial raw Watson HTTP response text."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text
```

---

## Question 3 (TEXT — actual IBM Lab output required)

The previous submission received 0 because it was an **offline mock at the wrong path**.
Run `bash run_in_ibm_lab.sh` in the IBM Lab after the files are updated, then paste the **actual terminal transcript** from `evidence/2b_application_creation.txt`. It must show `/home/project/final_project`, `python3`, the exact `from emotion_detection import emotion_detector` import, `print(emotion_detector('I am really mad about this'))`, `exit()`, and `python3 test_emotion_detection.py`. Do not substitute fabricated Watson response data.

----------------------------------------------------------------------
Ran 7 tests in 0.003s

OK

This is NOT the /home/project/final_project terminal output requested by the grading rubric. Re-run on IBM Lab.
```

---

## Question 4 (TEXT)

```python
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
```

---

## Question 5 (TEXT)

```text
OFFLINE EXAMPLE MODE (NOT IBM WATSON OUTPUT); working directory: /mnt/data/oaqjp-final-project-emb-ai
$ EMOTION_DETECTION_MOCK=1 python3 -c 'from EmotionDetection import emotion_detector; print(emotion_detector("I am glad this happened"))'
{'anger': 0.03, 'disgust': 0.03, 'fear': 0.03, 'joy': 0.88, 'sadness': 0.03, 'dominant_emotion': 'joy'}
```

---

## Question 6 (URL)

Verified public repository URL:
https://github.com/tdao7/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py

STATUS: 1/1 in grading. Keep this URL unchanged.

---

## Question 7 (TEXT)

```text
OFFLINE EXAMPLE MODE (NOT IBM WATSON OUTPUT); working directory: /mnt/data/oaqjp-final-project-emb-ai
$ EMOTION_DETECTION_MOCK=1 python3 -c 'from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector("I am very angry"))'
{'anger': 0.88, 'disgust': 0.03, 'fear': 0.03, 'joy': 0.03, 'sadness': 0.03, 'dominant_emotion': 'anger'}

This is not a live Watson result; run on IBM Lab for authentic output.
```

---

## Question 8 (TEXT)

```python
"""Unit tests for Watson Emotion Detection (isolated from live API)."""

import os
import unittest
from unittest.mock import patch

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Validate the five dominant emotions and invalid-input handling."""

    def setUp(self):
        """Ensure tests always validate parsing real-shaped HTTP responses."""
        self.previous_mock = os.environ.pop("EMOTION_DETECTION_MOCK", None)

    def tearDown(self):
        """Restore any user's mock setting."""
        if self.previous_mock is not None:
            os.environ["EMOTION_DETECTION_MOCK"] = self.previous_mock

    def _assert_dominant(self, text, dominant):
        """Use an HTTP fixture that mimics the Watson response format."""
        names = ("anger", "disgust", "fear", "joy", "sadness")
        scores = {name: (0.80 if name == dominant else 0.05) for name in names}
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            post.return_value.status_code = 200
            post.return_value.json.return_value = {
                "emotionPredictions": [{"emotion": scores}]
            }
            output = emotion_detector(text)
            post.assert_called_once()
        self.assertEqual(output["dominant_emotion"], dominant)
        for name in names:
            self.assertIsInstance(output[name], float)

    def test_joy(self):
        """Joy must be selected for its corresponding prediction."""
        self._assert_dominant("I am glad this happened", "joy")

    def test_anger(self):
        """Anger must be selected for its corresponding prediction."""
        self._assert_dominant("I am really mad about this", "anger")

    def test_disgust(self):
        """Disgust must be selected for its corresponding prediction."""
        self._assert_dominant("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """Sadness must be selected for its corresponding prediction."""
        self._assert_dominant("I am so sad about this", "sadness")

    def test_fear(self):
        """Fear must be selected for its corresponding prediction."""
        self._assert_dominant("I am really afraid that this will happen", "fear")

    def test_http_400(self):
        """Watson 400 returns None for all fields, including dominant emotion."""
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            post.return_value.status_code = 400
            output = emotion_detector("invalid data")
            post.assert_called_once()
        self.assertIsNone(output["dominant_emotion"])
        for name in ("anger", "disgust", "fear", "joy", "sadness"):
            self.assertIsNone(output[name])

    def test_blank_text(self):
        """Blank text is rejected without contacting Watson."""
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            output = emotion_detector("   ")
            post.assert_not_called()
        self.assertIsNone(output["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
```

---

## Question 9 (TEXT)

```text
Actual unit-test run (HTTP calls patched; not a live Watson API validation):
$ python3 -m unittest -v test_emotion_detection.py
test_anger (test_emotion_detection.TestEmotionDetection.test_anger)
Anger must be selected for its corresponding prediction. ... ok
test_blank_text (test_emotion_detection.TestEmotionDetection.test_blank_text)
Blank text is rejected without contacting Watson. ... ok
test_disgust (test_emotion_detection.TestEmotionDetection.test_disgust)
Disgust must be selected for its corresponding prediction. ... ok
test_fear (test_emotion_detection.TestEmotionDetection.test_fear)
Fear must be selected for its corresponding prediction. ... ok
test_http_400 (test_emotion_detection.TestEmotionDetection.test_http_400)
Watson 400 returns None for all fields, including dominant emotion. ... ok
test_joy (test_emotion_detection.TestEmotionDetection.test_joy)
Joy must be selected for its corresponding prediction. ... ok
test_sadness (test_emotion_detection.TestEmotionDetection.test_sadness)
Sadness must be selected for its corresponding prediction. ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.003s

OK
```

---

## Question 10 (TEXT)

```python
"""Serve the emotion detection web application with Flask."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the project's browser interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the supplied text and display a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## Question 11 (UPLOAD)

REQUIRES ACTUAL SCREENSHOT: `6b_deployment_test.png` of Flask web application running in IBM Lab and correctly displaying an emotion prediction. A separate `6b_deployment_preview.png` is only an OFFLINE UI MOCK preview and is NOT proof of deployment.

---

## Question 12 (TEXT)

```python
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
```

---

## Question 13 (TEXT)

```python
"""Serve the emotion detection web application with Flask."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the project's browser interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the supplied text and display a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## Question 14 (UPLOAD)

REQUIRES ACTUAL SCREENSHOT: `7c_error_handling_interface.png` of Flask web app rejecting blank input in IBM Lab. `7c_error_handling_preview.png` is only an OFFLINE UI MOCK preview and is NOT proof of deployment.

---

## Question 15 (TEXT)

```python
"""Serve the emotion detection web application with Flask."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def home():
    """Render the project's browser interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze the supplied text and display a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## Question 16 (TEXT — actual Pylint output required)

After running `bash run_in_ibm_lab.sh` in the IBM Lab, paste the contents of `evidence/8b_static_code_analysis.txt` containing the **actual** `pylint server.py` report and score. The assignment expects 10.00/10. Do not claim that score before the command actually reports it.

---

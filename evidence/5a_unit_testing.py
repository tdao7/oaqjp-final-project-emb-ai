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

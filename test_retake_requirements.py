"""Offline checks of the exact requirements flagged by the grader."""

import ast
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


class TestRetakeRequirements(unittest.TestCase):
    """Check the initial detector response and Flask configuration."""

    def test_task2_returns_text(self):
        """The initial detector must return response.text, not JSON parsing."""
        task2 = runpy.run_path(str(ROOT / "evidence/2a_emotion_detection.py"))
        with patch("requests.post") as mocked_post:
            mocked_post.return_value.text = '{"status":"ok"}'
            mocked_post.return_value.json.side_effect = AssertionError("Do not parse JSON")
            self.assertEqual(task2["emotion_detector"]("text"), '{"status":"ok"}')
            mocked_post.assert_called_once()

    def test_flask_import_and_host(self):
        """Flask imports the precise module path and listens on all interfaces."""
        tree = ast.parse((ROOT / "server.py").read_text())
        imports = [node.module for node in tree.body if isinstance(node, ast.ImportFrom)]
        self.assertIn("EmotionDetection.emotion_detection", imports)
        runs = [node for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "run"]
        self.assertEqual(len(runs), 1)
        arguments = {item.arg: item.value.value for item in runs[0].keywords}
        self.assertEqual(arguments, {"host": "0.0.0.0", "port": 5000})


if __name__ == "__main__":
    unittest.main()

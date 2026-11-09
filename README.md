# Final Project

## Emotion Detection with Watson NLP and Flask

This repository contains the IBM Skills Network final project for the course on
AI applications with Python and Flask. The project is based on the original
[IBM starter repository](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai).

The application classifies text across five emotions: anger, disgust, fear,
joy, and sadness. It shows the individual scores and the dominant emotion.

### Setup (IBM Skills Network lab or a computer with internet access)

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest -v test_emotion_detection.py
python3 server.py
```

Then open http://127.0.0.1:5000/ in your browser.

**Important:** The default detector calls the live IBM Watson NLP endpoint,
which may require the Skills Network lab network. If the endpoint is
unavailable, it will raise a service-related exception; it does not silently
substitute predictions. For a clearly marked, offline demonstration only:

```bash
EMOTION_DETECTION_MOCK=1 python3 server.py
```

Offline example mode uses *rule-based illustrative scores*, **not real Watson
predictions**. Unit tests use mocked HTTP responses to verify correct handling
of the Watson response format and errors without an external network.

### Required project files

- `EmotionDetection/emotion_detection.py`: Watson emotion analysis, output formatting, 400 response handling.
- `EmotionDetection/__init__.py`: exports `emotion_detector` as a Python package.
- `emotion_detection.py`: compatibility wrapper for the earlier task's import.
- `test_emotion_detection.py`: unit tests for the five emotions and error handling.
- `server.py`: Flask HTTP server, including empty-input validation.
- `templates/index.html`, `static/mywebscript.js`: web interface.
- `evidence/`: task-by-task evidence and initial snapshots.
- `ANSWERS.md`: all 16 submission fields and what to paste/upload.

### Publishing the required public fork

The assignment specifically requires a **public fork** named
`oaqjp-final-project-emb-ai` under your own GitHub account. This ZIP is
source code only; do not submit a prospective GitHub URL until you have
actually forked and pushed the project. After authenticating GitHub CLI with
`gh auth login`, run `bash publish_tdao7.sh` from the extracted directory.
This script creates/reuses the fork and uploads your project files.

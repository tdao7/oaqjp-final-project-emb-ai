# Retake guide — graded 9/16, need 12/16 to pass

## Already passed
Questions 1, 4, 5, 6, 7, 8, 9, 12, 13. Do not need to redo.

## Revised answers
- Question 2: paste `evidence/2a_emotion_detection.py` (key fix: `return response.text`).
- Question 10: paste `server.py` (key fixes: exact package import and `host="0.0.0.0"`).
- Question 15: paste `server.py`, preserving all Python indentation and docstrings.

## Authentic output and screenshots are still required
- Question 3: run `bash run_in_ibm_lab.sh` in `/home/project/final_project`, paste the genuine captured terminal transcript from `evidence/2b_application_creation.txt`. Do not replace with mocked text.
- Question 11: while Flask is running at `http://127.0.0.1:5000/`, enter a sentence such as `I am really happy today!`, click the analysis button, verify real emotion response, then take a browser screenshot including address bar, input, and result as `6b_deployment_test.png`.
- Question 14: leave the input blank and click Analyze, capture the visible `Invalid text! Please try again!` at the same live Flask URL in `7c_error_handling_interface.png`.
- Question 16: paste real contents of `evidence/8b_static_code_analysis.txt`, captured from `python3 -m pylint server.py` in IBM Lab. If it is below 10/10, fix lint warnings and rerun before submitting.

## Publish corrected code to your public fork
Current GitHub connector returned HTTP 403 on writes, despite repo `tdao7/oaqjp-final-project-emb-ai` being public. From this extracted directory on your authenticated machine, run `bash apply_fixes_tdao7.sh`. This pulls and updates that fork, runs offline unit tests, commits and pushes only the listed corrected files.

## Truthfulness
The old `*_preview.png` files are **not** deployment evidence and must not be uploaded for questions 11 or 14. Their replacement screenshots must come from a running Flask application. Unit-test fixtures and the optional `EMOTION_DETECTION_MOCK=1` mode are not real Watson predictions.

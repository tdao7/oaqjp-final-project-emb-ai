#!/usr/bin/env bash
# Run this IN THE ACTUAL IBM Skills Network Lab to collect real, not mocked evidence.
set -euo pipefail
cd /home/project/final_project
mkdir -p evidence
printf 'Verified working directory: '; pwd
python3 -m pip install -r requirements.txt
printf '\n=== Task 2b: Live Watson interactive shell and unit tests ===\n'
{
  pwd
  printf '$ python3\n'
  python3 -i <<'PY'
from emotion_detection import emotion_detector
print(emotion_detector('I am really mad about this'))
exit()
PY
  printf '$ python3 test_emotion_detection.py\n'
  python3 test_emotion_detection.py
} 2>&1 | tee evidence/2b_application_creation.txt
printf '\n=== Task 8b: Real Pylint output ===\n'
python3 -m pylint server.py 2>&1 | tee evidence/8b_static_code_analysis.txt
printf '\n=== Flask server ===\n'
printf 'Open http://127.0.0.1:5000 and capture evidence/6b_deployment_test.png and evidence/7c_error_handling_interface.png\n'
python3 server.py

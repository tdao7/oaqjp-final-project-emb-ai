# Commands to run in the official IBM Skills Network Lab

The assignment screenshots demand terminal evidence from `/home/project/final_project`.
The files generated in this environment **cannot legitimately claim that path**.
To collect authentic evidence in the lab:

```bash
cd /home/project/final_project
python3 -m pip install -r requirements.txt
python3
>>> from emotion_detection import emotion_detector
>>> print(emotion_detector('I am really mad about this'))
>>> exit()
python3 test_emotion_detection.py
python3 -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am very angry'))"
python3 server.py
```

Open the lab's **Skills Network Web Preview**, type a text expression,
press **Run Sentiment Analysis**, and save the actual browser screenshot as
`6b_deployment_test.png`. Then enter blank text and save
`7c_error_handling_interface.png`.

Run the pylint assessment:
```bash
python3 -m pylint server.py
```

Copy your **actual** terminal output into the text fields for questions 3,
5, 7, 9 and 16 (the files `evidence/` show what is expected). The remote
Watson API requires live network access; no claim of live correctness is
made for local offline mock tests.

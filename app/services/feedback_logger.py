import json
import os

FEEDBACK_FILE = "feedback.json"


def save_feedback(data):

    feedback = []

    if os.path.exists(FEEDBACK_FILE):

        try:
            with open(FEEDBACK_FILE, "r") as f:
                feedback = json.load(f)

        except:
            feedback = []

    feedback.append(data)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback, f, indent=4)
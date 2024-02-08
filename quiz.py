import json
import sys


class Quiz:
    with open("questions.json") as file:
        data = json.load(file)
    
    # All questions and entering answers occur here
    @classmethod
    def do_quiz(cls):
        for i, question in enumerate(cls.data):
            # Ask 1 question at a time
            cls._ask_question(i, question["question"])
    
    # PRIVATE METHODS
    @staticmethod
    def _ask_question(num, question):
        print(f"Q{num + 1}) {question}")


# Testing Purposes
if __name__ == "__main__":
    q = Quiz()
    Quiz.do_quiz()
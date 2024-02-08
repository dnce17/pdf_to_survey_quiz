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

            # Show choices for question
            cls._show_choices(question["choices_and_traits"])

            # Loop until user enters elgible answer
            while True:
                total_choices = len(question["choices_and_traits"])
                ans = cls._get_ans()
                if cls._validate_ans(ans, total_choices) == True:
                    break
    
    # PRIVATE METHODS
    @staticmethod
    def _ask_question(num, question):
        print(f"Q{num + 1}) {question}")
    
    @staticmethod
    def _show_choices(choices_arr):
        for i, choice_trait in enumerate(choices_arr):
            choice = choice_trait[0]
            print(f"{i + 1} - {choice}")
    
    @staticmethod
    def _get_ans():
        return input("Enter a number that corresponds with the choices: ")
    
    @staticmethod
    def _validate_ans(ans, total_choices):
        try:
            if int(ans) not in range(1, total_choices + 1):
                return False
        except ValueError:
            return False
        
        return True


# Testing Purposes
if __name__ == "__main__":
    q = Quiz()
    Quiz.do_quiz()
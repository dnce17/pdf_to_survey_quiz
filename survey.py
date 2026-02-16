import json
import re

class Survey:
    def __init__(self, survey, respondent=None):
        self.survey = json.load(open(survey))
        self.respondent = respondent
    
    def do_survey(self):
        """Ask questions and enter answers until survey is done, then show results"""
        for i, question in enumerate(self.survey):
            # Ask 1 question at a time
            self._ask_question(i, question["question"])

            # Show choices for question
            self._show_choices(question["choices_and_traits"])

            # Loop until user enters elgible answer
            while True:
                total_choices = len(question["choices_and_traits"])
                ans = self._get_ans()
                if self._validate_ans(ans, total_choices) == True:
                    trait_arr = question["choices_and_traits"][int(ans) - 1][1:]
                    self.respondent._add_trait_pts(*trait_arr)
                    break
        
        self.respondent._show_results()
        print()


    # NON-PRIVATE METHODS
    def get_each_trait_count(self):
        """Get total count of each trait"""
        traits = {}
        for _, question in enumerate(self.survey):
            for _, choice_trait in enumerate(question["choices_and_traits"]):
                # Uses [1:] b/c some choices are linked with more than 1 trait
                for trait in choice_trait[1:]:
                    trait_formatted = trait.strip().lower()
                    if trait_formatted not in traits:
                        traits[trait_formatted] = 1
                    else:
                        traits[trait_formatted] += 1
        
        return dict(sorted(traits.items()))
    
    def show_each_trait_count(self):
        """Print the results from get_each_trait_count()"""
        print(f"Total Count of Each Trait: {self.get_each_trait_count()}")

    def get_all_traits(self):
        return [trait for trait in self.get_each_trait_count()]
    
    def show_all_traits(self, ordered_list = False):
        print("All Traits in This Survey:")
        if ordered_list == True:
            for i, item in enumerate(self.get_all_traits()):
                print(f"{i + 1}) {item}")
        else:
            print(self.get_all_traits())
    

    # PRIVATE METHODS
    @staticmethod
    def _ask_question(num, question):
        print(f"\nQ{num + 1}) {question.strip()}")
    
    @staticmethod
    def _show_choices(choices_arr):
        for i, choice_trait in enumerate(choices_arr):
            choice = choice_trait[0]
            print(f"{i + 1} - {choice.strip()}")
    
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


class Respondent():
    def __init__(self):
        pass
    
    def traits_to_track(self, test_traits):
        """
        Dynamically creates instance (self) attributes for each trait in the survey
        and initializes their counts to 0.

        This avoids hardcoding instance attributes in __init__.
        """
        for trait in test_traits:
            print('traits_to_track func activate')
            setattr(self, f"_{re.sub(r'[ -]', '_', trait).lower()}", 0)

    def get_results(self):
        """Return a dictionary of all instance attributes (aka traits) and their current values"""
        return vars(self)
    
    def _add_trait_pts(self, *traits):
        for trait in [trait.strip().lower() for trait in traits]:
            attr_name = f"_{re.sub(r'[ -]', '_', trait)}"
            # Use formatted attr_name to get current value of that trait on the instance
            trait_attr = getattr(self, attr_name)
            # Increase the trait's value by 1
            setattr(self, attr_name, trait_attr + 1)

    def _show_results(self):
        results_list = sorted(self.get_results().items(), key=lambda trait: trait[1], reverse=True)
        print("\nRESULTS:")
        for trait in dict(results_list):
            print(f"{trait.lstrip('_').title().replace('_', ' ')}: {vars(self)[trait]}")
            print(f"Vars print: {vars(self)}")


# TEST Purposes - delete before pushing
if __name__ == "__main__":
    user = Respondent()
    survey = Survey("questions.json", user)
    user.traits_to_track(survey.get_all_traits())

    # survey.show_all_traits()
    # survey.get_each_trait_count()
    # survey.show_each_trait_count()
    # survey.show_all_traits(ordered_list=True)
    user._show_results()
    # print(sorted(user.get_results(), key=lambda trait: trait))
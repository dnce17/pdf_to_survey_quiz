# coding: utf-8 at top here to allow non-ASCII char like dark circle bullet or else error occurs
# -*- coding: utf-8 -*-
import sys
import csv
import os
import pdfplumber
import json
from survey import Survey, Respondent
from itertools import chain


IDENTIFIERS = {
    "bullets": ["• ", "● "],
    "sub_bullets_1": ["o ", "○ "],
    "sub_bullets_2": ["▪ ", "■ "]
}
EDGE_CASE_ESCAPE = "~o " # Prevents lines starting with words that begin with "o" from being mistaken for an "o" sub-bullet
DEFAULT_JSON_NAME = "questions.json"
ARGV_LEN = [2,3]


def main():
    if argv_issue := check_cmd_args(sys.argv):
        sys.exit(argv_issue)

    # Stage 1: Convert survey to json
    pdf_file = open_file(sys.argv[1])
    text_arr = get_text(pdf_file)
    survey_items = filter_text(text_arr)

    # Compile questions, answers, and traits from arr into json
    make_json(compile_survey(survey_items))

    # Stage 2: Ensure traits to track are correct
    user = Respondent()
    survey = Survey(DEFAULT_JSON_NAME, user)

    survey.show_all_traits(ordered_list = True)
    while ask_user(
        "Are the traits to be tracked correct? Type and enter y/n: ", 
        "\nExiting program....Ensure your PDF doc has no misspelled traits and is correctly formatted.\n"
    ) == False:
        continue

    # Stage 3: Doing survey
    while ask_user(
        "Type \"y\" to start the survey or \"n\" if not: ",
        "\nExiting program....Respondent not ready yet.\n"
    ) == False:
        continue

    user.traits_to_track(survey.get_all_traits())
    survey.do_survey()

    # Stage 4: Save result to csv file, if desired
    if len(sys.argv) == max(ARGV_LEN):
        while True:
            name = get_name()
            if confirm_name(" ".join(name)) == True:
                break

        # Create directory to store csv, if nonexistent
        csv_dir_name = "csv_files"
        if check_path_exist(csv_dir_name) == False:
            create_csv_dir(csv_dir_name)
        
        # Create csv file if it does not exist
        csv_file = sys.argv[2]
        fieldnames = create_fieldnames(["first_name", "last_name"], sorted(user.get_results(), key=lambda trait: trait, reverse=True))
        if check_path_exist(f"csv_files/{csv_file}") == False:
            create_csv_file(csv_file)

            # Add header to file
            add_csv_headers(f"csv_files/{csv_file}", fieldnames)

        store_results(name, user.get_results(), f"csv_files/{csv_file}", fieldnames)
            

def check_cmd_args(cmd_args):
    if check_argv_len(cmd_args) == False:
        return "usage: main.py path_to_PDF_file.pdf [OPTIONAL_csv_file_to_save_to].csv"
    elif len(cmd_args) == max(ARGV_LEN) and has_csv_ext(cmd_args[2]) == False:
        return "Exiting program....Ensure csv file to save to has .csv extension"
    

def check_argv_len(cmd_args):
    if len(cmd_args) not in ARGV_LEN:
        return False


def has_csv_ext(csv_file_name):
    if os.path.splitext(csv_file_name)[1] != ".csv":
        return False


def open_file(f):
    try:
        file = pdfplumber.open(f)
    except FileNotFoundError: 
        sys.exit("File not found. Also ensure that extension is .pdf")
    
    return file


def get_text(f):
    lines_arr = []
    with f as pdf:
        for pg in pdf.pages:
            pdf_text = pg.extract_text(x_tolerance=1)
            # \n to get each line
            lines = pdf_text.split('\n')
            for _, line in enumerate(lines):
                lines_arr.append(line)
    
    return lines_arr


def filter_text(arr):
    # Remove everything before ---questions--- string in array
    question_section = find_question_start_point(arr)

    # Combine fragmented sentences that were split from line break
    survey_items = combine_frag(question_section)

    return survey_items


def find_question_start_point(arr):
    """
    Only returns all items in the list that appear after the '---questions---'
    string, which indicates where survey questions begin
    """
    try:
        # Search for ---questions-- string case-insensitive
        index = [item.lower().strip() for item in arr].index('---questions---')
    except ValueError:
        sys.exit("Ensure that ---questions--- is present in your PDF to help indicate where questions begin")

    return arr[index + 1:]


def combine_frag(arr):
    """
    Combines fragmented sentences
    Example:
        ["o First line", "continues here", "o Second line"] turns into ["o First line continues here", "o Second line"]
    """
    updated_arr = []
    for _, item_str in enumerate(arr):
        if item_str[0:2] in list(chain(*IDENTIFIERS.values())):
            updated_arr.append(item_str)
        else:
            if item_str[0:3] == EDGE_CASE_ESCAPE:
                # Remove the "~" escape marker, treating "~o" as normal letter "o"
                updated_arr[-1] += f" {item_str.replace('~', '')}"
            else:
                # Combine fragmented sentences together as 1 item in arr
                updated_arr[-1] += f" {item_str}"
    
    return updated_arr


def compile_survey(arr):
    survey_data = []
    current_question = {
        "question": "",
        "choices_and_traits": []
    }

    for i, line in enumerate(arr):
        if line[0:2] in IDENTIFIERS["bullets"]:
            if i > 0:
                survey_data.append(current_question.copy())

            # New bullet means new question, so reset choices_and_traits 
            current_question["question"] = line[2:]
            current_question["choices_and_traits"] = []

        elif line[0:2] in IDENTIFIERS["sub_bullets_1"]:
            # Append answer choice
            current_question["choices_and_traits"].append([line[2:]])
        elif line[0:2] in IDENTIFIERS["sub_bullets_2"]:
            # Append trait to answer choice
            current_question["choices_and_traits"][-1].append(line[2:].title())
        
        if i == len(arr) - 1:
            # Append the last question b/c loops ends after this, so i > 0 wouldn’t trigger
            survey_data.append(current_question.copy())

    return survey_data


def make_json(dict_arr):
    with open(DEFAULT_JSON_NAME, 'w') as output:
        json.dump(dict_arr, output, indent=2)


def ask_user(prompt_msg, exit_msg):
    prompt = input(prompt_msg).strip().lower()
    if prompt in ["y", "yes"]:
        return True
    elif prompt in ["n", "no"]:
        sys.exit(exit_msg)
    else:
        return False


def get_name():
    first_name = input("First Name: ").strip().title()
    last_name = input("Last Name: ").strip().title()
    return [first_name, last_name]


def confirm_name(name):
    while True:
        confirmation = input(f"Is {name} correct? Type and enter y/n: ").strip().lower()
        if confirmation not in ["y", "yes", "n", "no"]:
            continue
        
        return True if confirmation in ["y", "yes"] else False


def check_path_exist(path):
    return True if os.path.exists(path) else False
        

def create_csv_dir(dir_name):
    os.makedirs(dir_name)


def create_csv_file(file_name):
    try:
        file = open(f"csv_files/{file_name}", "x")
        file.close()
    except FileExistsError:
        return


def create_fieldnames(*arrs):
    finished_arr = []
    for arr in arrs:
        finished_arr.extend(arr)
    return finished_arr


def add_csv_headers(file, header_names):
    with open(file, "a") as file:
        writer = csv.DictWriter(file, fieldnames=header_names)
        writer.writeheader()


def store_results(name, result, csv_file, header_names):
    with open(csv_file, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header_names)
        row_info = {"first_name": name[0], "last_name": name[1]}
        row_info.update(dict(result))

        writer.writerow(row_info)


if __name__ == "__main__":
    main()
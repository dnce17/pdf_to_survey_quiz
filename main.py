import sys
import pdfplumber
import json


IDENTIFIERS = ["• ", "o ", "▪ "]
EDGE_CASE_ESCAPE = "~o "


def main():
    # Testing, but when done, make file be entered from cmd line
    pdf_file = open_file("test_files/test_file1.pdf")
    # pdf_file = open_file("test_files/test_file3.pdf")
    text_arr = get_text(pdf_file)
    quiz_items = filter_text(text_arr)

    # Compile questions, ans, and traits from arr into json
    make_json(compile_quiz(quiz_items))


def open_file(f):
    try:
        file = pdfplumber.open(f)
    except FileNotFoundError: 
        sys.exit("File not found")
    
    return file


def get_text(f):
    lines_arr = []
    with f as pdf:
        for pg in pdf.pages:
            pdf_text = pg.extract_text()
            # \n to get each line
            lines = pdf_text.split('\n')
            for _, line in enumerate(lines):
                lines_arr.append(line)
    
    return lines_arr


def filter_text(arr):
    # Remove everything before "---questions---"" in arr
    first_filter = remove_unrelated(arr)

    # Combine fragmented sentences that were split from line break
    quiz_items = combine_frag(first_filter)

    return quiz_items


def remove_unrelated(arr):
    try:
        # Search ---questions-- case-insensitive
        index = [item.lower().strip() for item in arr].index('---questions---')
    except ValueError:
        sys.exit("Ensure that ---questions--- is present in your PDF to help indicate where questions begin")

    return arr[index + 1:]


def combine_frag(arr):
    updated_arr = []
    for _, item in enumerate(arr):
        if item[0:2] in IDENTIFIERS:
            # Append b/c "in IDENTIFIERS" means it's a new bullet (hence, new item in arr)
            updated_arr.append(item)
        else:
            # ~o is escape char to differentiate b/w o sub-bullet vs starting o in new line
            if item[0:3] == EDGE_CASE_ESCAPE:
                updated_arr[-1] += f" {item.replace('~', '')}"
            else:
                # Combine fragmented sentences together as 1 item in arr
                updated_arr[-1] += f" {item}"
    
    return updated_arr


def compile_quiz(arr):
    dict_arr = []
    dict = {
        "question": "",
        "choices_and_traits": []
    }

    for i, line in enumerate(arr):
        if line[0:2] == IDENTIFIERS[0]:
            if i > 0:
                dict_arr.append(dict.copy())

            # Reset choices_and_traits if new question (aka new bullet)
            dict["question"] = line[2:]
            dict["choices_and_traits"] = []

        elif line[0:2] == IDENTIFIERS[1]:
            dict["choices_and_traits"].append([line[2:]])
        elif line[0:2] == IDENTIFIERS[2]:
            dict["choices_and_traits"][-1].append(line[2:].title())
        
        # Appends the last question to arr b/c no more new questions (bullets) after
        if i == len(arr) - 1:
            dict_arr.append(dict.copy())

    return dict_arr


def make_json(dict_arr):
    with open('questions.json', 'w') as output:
        json.dump(dict_arr, output, indent=2)
        

if __name__ == "__main__":
    main()
import sys
import pdfplumber


IDENTIFIERS = ["• ", "o ", "▪ "]


def main():
    # Testing, but when done, make file be entered from cmd line
    pdf_file = open_file("test_files/test_file.pdf")
    text_arr = get_text(pdf_file)
    quiz_items = filter_text(text_arr)

    # Compile questions, ans, and traits from arr into json
    compile_quiz(text_arr)

    # Funcs to make next (subject to change)
    # make_questions(extracted_text)


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
    for item in quiz_items:
        print(item)


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
            # Combine fragmented sentences together as 1 item in arr
            updated_arr[-1] += f" {item}"
    
    return updated_arr


def compile_quiz(text_arr):
    ...

    # Read through each line of arr
    # Add to json and make it a question, ans choice, or trait depending on leading bullet type (might add other list types too)
        

if __name__ == "__main__":
    main()
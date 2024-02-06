import sys
import pdfplumber


def main():
    # Testing, but when done, make file be entered from cmd line
    pdf_file = open_file("test_file.pdf")
    text_arr = get_text(pdf_file)

    # Compile questions, ans, and traits from arr into json
    compile_quiz(text_arr)

    # Draft funcs
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


def compile_quiz(text_arr)
    ...

if __name__ == "__main__":
    main()
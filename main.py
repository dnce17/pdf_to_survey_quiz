import sys
import pdfplumber


def main():
    # Testing, but when done, make file be entered from cmd line
    pdf_file = open_file("test_q.pdf")
    extracted_text_arr = get_text(pdf_file)

    # Draft funcs
    # make_questions(extracted_text)


def open_file(f):
    try:
        file = pdfplumber.open(f)
    except FileNotFoundError: 
        sys.exit("File not found")
    
    return file


if __name__ == "__main__":
    main()
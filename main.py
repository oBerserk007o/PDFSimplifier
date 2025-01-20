#!/usr/bin/env python3
# coding: utf8

import logging
try:
    import os
    from time import strftime
    from os import listdir
    from os.path import isfile, join
    from pypdf import PdfReader
except ImportError:
    print("Something went wrong")
    logging.exception("Something went wrong")
    exit()

from segmenter import main_segmenter, choose_pdf_index, choose_segmentation_index, choose_start_end_indexes
from simplifier import mainloop_simplifier, load_segments, choose_language, choose_model, compile_texts
from compiler import choose_font, write_to_pdf
from checks import check_dirs, check_key


logging.basicConfig(
    filename=f"{strftime('%Y%m%d_%H%M%S')}.log",
    encoding="utf-8",
    filemode="a",
    format="[{asctime}] {levelname}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

logging.info("Application starting")

try:
    os.system("cls")
except:
    print("Something went wrong, are you on Linux/Mac?")
    logging.exception("Something went wrong, are you on Linux/Mac?")


print("Welcome to PDFSimplifier!")
print("This is a program that takes in a pdf, segments it into smaller more digestible pieces, sends them to ChatGPT to simplify the vocabulary and recompiles the bits into one big text you can read more easily!\n")
print("By using this software, you agree to the license stated in 'LICENSE'\n")
print("DISCLAIMER: This program may not work on Linux/Mac!\n")
print("If something goes wrong, try restarting the program, if it still doesn't work, restart your device")
print("If it's still not working, please contact me with the according log file (which is often the latest)")
print("You can contact me at {email}\n")
print("To make an API key for OpenAPI (which is necessary for this program), follow this guide: "
      "https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/")
print("The source code can be found at 'https://github.com/oBerserk007o/PDFSimplifier/tree/master?tab=MIT-1-ov-file'\n\n")
print("It is suggested that you put the program in an isolated directory to avoid erasing present files\n")
print("Press Ctrl+C to exit at any time\n\n")

logging.info("Notified user")

# checks
files_dirs = {
    "pdf": "no",
    "result": "",
    "segmented_output": "",
    "fonts": "",
    "key.txt": ""
}
check_dirs(files_dirs)
check_key()
logging.info("Checks passed successfully")


# TODO: confirm settings before each big step
# TODO: transform into executable
# TODO: step by step, choose where to start from


try:
    # segmenter
    segmentation_options = ["sentence", "page"]
    pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]
    print("\nDISCLAIMER: Make sure the PDF file contains actual text, and not photos of text, in which case, the program will NOT work\n")
    index = choose_pdf_index(pdfs)
    pdf_name = pdfs[index]
    segmentation_index, count = choose_segmentation_index(segmentation_options)

    reader = PdfReader(f"pdf/{pdfs[index]}")
    start, end = choose_start_end_indexes(reader)

    main_segmenter(segmentation_index, count, start, end, reader)
    logging.info("Segmentation done from main")

    # simplifier
    text_segments = load_segments()
    chosen_language = choose_language()
    chosen_model = choose_model(text_segments, chosen_language)
    mainloop_simplifier(text_segments, chosen_model, chosen_language)
    logging.debug("Simplifying done, compiling")
    exported_file_name = compile_texts(chosen_model)
    logging.info("Process finished, asking to clear files")

    # compiler
    choose_font()
    write_to_pdf(pdf_name, exported_file_name)
    #write_to_pdf("pdf_name.pdf", "simplified_text1-gpt-4o-mini.txt")
    print(f"\nThe simplified text is in '{'simplified_' + 'pdf_name.pdf'}'")
    print(f"Please move it to another directory, since it may get erased or cause errors if you run the program again\n")

    # clearing files
    clear_segmented_output = not "n" in input("Would you like to clear the 'segmented_output' directory? (y/N) > ").lower()
    clear_result = not "n" in input("Would you like to clear the 'result' directory? (y/N) > ").lower()

    if clear_segmented_output:
        for file in [f for f in listdir("segmented_output") if isfile(join("segmented_output", f))]:
            os.remove(f"segmented_output/{file}")
    if clear_result:
        for file in [f for f in listdir("result") if isfile(join("result", f))]:
            os.remove(f"result/{file}")

    print("Thank you for using PDFSimplifier!\n")

except KeyboardInterrupt:
    print("\nExiting")
    logging.info("User exited program")
except:
    print("\nSomething went wrong")
    logging.exception("Something went wrong")

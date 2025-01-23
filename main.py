#!/usr/bin/env python3
# coding: utf8

import logging
import os
import sys
from time import strftime
from os import listdir
from os.path import isfile, join
from pypdf import PdfReader
from segmenter import main_segmenter, choose_pdf_index, choose_segmentation_index, choose_start_end_indexes
from simplifier import mainloop_simplifier, load_segments, choose_language, choose_model, compile_texts
from compiler import choose_font, write_to_pdf
from checks import check_dirs, check_key, confirm_settings, smart_input

# python -m PyInstaller --onefile --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext main.py

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
pdf_name = "text.pdf"
starting_options = ["Normal run (choose this if this is your first time running this program)",
                    "Just segment the pdf",
                    "Just simplify, I already segmented the pdf",
                    "Just turn it into a pdf, I already simplified the text",
                    "Just clear the files"]

try:
    os.system("cls")
except:
    print("Something went wrong, are you on Linux/Mac?")
    logging.exception("Something went wrong, are you on Linux/Mac?")
    os.system("pause")


def notify_user():
    print("Welcome to PDFSimplifier!")
    print("This is a program that takes in a pdf, segments it into smaller more digestible pieces, sends them to ChatGPT to simplify the vocabulary, recompiles the bits into one big text file, and turns it into a pdf file you can read more easily!")
    print("By using this software, you agree to the license stated in 'LICENSE'\n")
    print("DISCLAIMER: This program may not work on Linux/Mac!\n")
    print("If something goes wrong, try restarting the program and making sure all the required files and directories are present, if it still doesn't work, restart your device")
    print("If it's still not working, please contact me with the according log file (which is often the latest)")
    print("You can contact me at 'frostbyte0x0@gmail.com'\n")
    print("To make an API key for OpenAPI (which is necessary for this program), follow this guide: "
          "https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/")
    print("The source code can be found at 'https://github.com/oBerserk007o/PDFSimplifier/tree/master?tab=MIT-1-ov-file'\n\n")
    print("It is suggested that you put the program in an isolated directory to avoid erasing present files\n")
    print("Press Ctrl+C to exit at any time\n\n")

    logging.info("Notified user")


def checks():
    files_dirs = {
        "pdf": "no",
        "result": "",
        "segmented_output": "",
        "fonts": "no",
        "key.txt": ""
    }
    check_dirs(files_dirs)
    check_key()
    logging.info("Checks passed successfully")


def list_starting_options():
    for i, option in enumerate(starting_options):
        print(f"{i}: {option}")


def choose_where_to_start():
    list_starting_options()
    return str(smart_input("Where do you want to start? > ", len(starting_options) - 1))


def segment():
    global pdf_name
    segmentation_options = ["sentence", "page"]
    pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]
    print("\nDISCLAIMER: Make sure the PDF file contains actual text, and not photos of text, in which case, the program will NOT work\n")
    index = choose_pdf_index(pdfs)
    pdf_name = pdfs[index]
    segmentation_index, count = choose_segmentation_index(segmentation_options)

    reader = PdfReader(f"pdf/{pdfs[index]}")
    start, end = choose_start_end_indexes(reader)

    confirmed = confirm_settings(
        {
            "PDF chosen": pdf_name,
            "Segmentation option": segmentation_options[segmentation_index],
            "Segmentation count": count
        }
    )
    if not confirmed:
        segment()

    main_segmenter(segmentation_index, count, start, end, reader)
    logging.info("Segmentation done from main")


def simplify(loaded_segments=None):
    if loaded_segments is None:
        text_segments = load_segments()
    chosen_language = choose_language()
    chosen_model = choose_model(text_segments, chosen_language)

    confirmed = confirm_settings(
        {
            "File language": chosen_language,
            "Model": chosen_model
        }
    )
    if not confirmed:
        simplify(text_segments)

    mainloop_simplifier(text_segments, chosen_model, chosen_language)
    logging.debug("Simplifying done, compiling")
    exported_file_name = compile_texts()
    logging.info("Process finished, asking to clear files")
    return exported_file_name


def compile_to_pdf(exported_file_name=None):
    if exported_file_name is None:
        exported_file_name = input("What is the name of the text file to turn into a pdf (without the file extension)? > ")

    try:
        with open(exported_file_name, "r", encoding="utf-8"):
            pass
    except FileNotFoundError:
        print(f"File '{exported_file_name}' not found")
        logging.exception(f"File '{exported_file_name}' not found, retrying")
        compile_to_pdf()
        return

    fonts = [f[:-4] for f in listdir("fonts") if isfile(join("fonts", f)) and f[-3:] == "ttf"]
    choose_font(fonts)
    write_to_pdf(pdf_name, exported_file_name)
    print(f"\nThe simplified text is in '{'simplified_' + pdf_name}'")
    print(f"Please move it to another directory, since it may get erased or cause errors if you run the program again\n")


def clear_directories():
    clear_segmented_output = "y" in input("Would you like to clear the 'segmented_output' directory? (y/N) > ").lower()
    clear_result = "y" in input("Would you like to clear the 'result' directory? (y/N) > ").lower()

    if clear_segmented_output:
        for file in [f for f in listdir("segmented_output") if isfile(join("segmented_output", f))]:
            os.remove(f"segmented_output/{file}")
    if clear_result:
        for file in [f for f in listdir("result") if isfile(join("result", f))]:
            os.remove(f"result/{file}")


def start_menu():
    print("\n")
    match choose_where_to_start().strip(" "):
        case "0":
            segment()
            exported_file = simplify()
            compile_to_pdf(exported_file)
            clear_directories()
        case "1":
            segment()
        case "2":
            simplify()
        case "3":
            compile_to_pdf()
        case "4":
            clear_directories()
        case _:
            print("Please enter a valid option number")
            start_menu()


try:
    notify_user()
    checks()
    start_menu()

    print("Thank you for using PDFSimplifier!\n")
    os.system("pause")

except KeyboardInterrupt:
    print("\nExiting")
    logging.info("User exited program")
except SystemExit:
    logging.info("Exiting from main, something happened")
    os.system("pause")
except:
    print("\nSomething went wrong")
    logging.exception("Something went wrong")
    os.system("pause")

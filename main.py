import os
import logging
from time import strftime
from os import listdir
from os.path import isfile, join
from pypdf import PdfReader
from segmenter import Segmenter
from simplifier import Simplifier
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
print("Press Ctrl+C to exit at any time\n\n")

logging.info("Notified user")

# checks
files_dirs = {
    "pdf": "no",
    "result": "",
    "segmented_output": "",
    "key.txt": ""
}
check_dirs(files_dirs)
check_key()
logging.info("Checks passed successfully")

try:
    # segmenter
    segmentation_options = ["sentence", "page"]
    pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]
    print("\nDISCLAIMER: Make sure the PDF file contains actual text, and not photos of text, in which case, the program will NOT work\n")
    segmenter = Segmenter(logging)
    index = segmenter.choose_pdf_index(pdfs)
    segmentation_index, count = segmenter.choose_segmentation_index(segmentation_options)

    reader = PdfReader(f"pdf/{pdfs[index]}")
    start, end = segmenter.choose_start_end_indexes(reader)

    segmenter.main_segmenter(segmentation_index, count, start, end, reader)
    logging.info("Segmentation done from main")

    # simplifier
    simplifier = Simplifier(logging)
    text_segments = simplifier.load_segments()
    chosen_language = simplifier.choose_language()
    chosen_model = simplifier.choose_model(text_segments, chosen_language)
    simplifier.mainloop_simplifier(text_segments, chosen_model, chosen_language)
    logging.debug("Simplifying done, compiling")
    simplifier.compile_texts(chosen_model)
    logging.info("Process finished, exiting")

except KeyboardInterrupt:
    print("\nExiting")
    logging.info("User exited program")
except:
    print("\nSomething went wrong")
    logging.exception("Something went wrong")

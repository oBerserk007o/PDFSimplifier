import os
from os import listdir
from os.path import isfile, join
from pypdf import PdfReader
from segmenter import main_segmenter, choose_pdf_index, choose_segmentation_index, choose_start_end_indexes
from simplifier import load_segments, choose_language, choose_model, mainloop_simplifier, compile_texts
from checks import check_dirs, check_key


# TODO:
#  - Smart input
#  - Logging

os.system("cls")

print("Welcome to PDFSimplifier!")
print("By using this software, you agree to the license stated in 'LICENSE'\n")
print("DISCLAIMER: This program may not work on Linux/Mac!\n")
print("If something goes wrong, please contact me with the according log file")
print("You can contact me at {email}")
print("To make an API key for OpenAPI (which is necessary for this program), follow this guide: https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/")
print("The source code can be found at 'https://github.com/oBerserk007o/PDFSimplifier/tree/master?tab=MIT-1-ov-file'")


# checks
files_dirs = {
    "pdf": "no",
    "result": "yes",
    "segmented_output": "",
    "key.txt": ""
}
check_dirs(files_dirs)
check_key()


# segmenter
segmentation_options = ["sentence", "page"]
pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]
print("\nDISCLAIMER: Make sure the PDF file contains actual text, and not photos of text, in which case, the program will NOT work\n")
index = choose_pdf_index(pdfs)
segmentation_index, count = choose_segmentation_index(segmentation_options)

reader = PdfReader(f"pdf/{pdfs[index]}")
start, end = choose_start_end_indexes(reader)

main_segmenter(segmentation_index, count, start, end, reader)


# simplifier
text_segments = load_segments()
chosen_language = choose_language()
chosen_model = choose_model(text_segments, chosen_language)
#mainloop_simplifier(text_segments, chosen_model, chosen_language)
#compile_texts()

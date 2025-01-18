from os import listdir
from os.path import isfile, join
from pypdf import PdfReader
from segmenter import main_segmenter, choose_pdf_index, choose_segmentation_index, choose_start_end_indexes
from simplifier import load_segments, choose_language, choose_model, mainloop_simplifier, compile_texts


# TODO:
#  - Checks:
#       - File/directory checking
#           - Present
#           - Empty
#       - Key checking
#           - Present
#           - Valid
#  - Smart input
#  - Logging


# segmenter
segmentation_options = ["sentence", "page"]
pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]
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

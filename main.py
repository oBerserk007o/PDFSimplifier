from pypdf import PdfReader
from os import listdir
from os.path import isfile, join


pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]

if len(pdfs) == 0:
    print("Please put a pdf in the 'pdf' directory")
    exit()


for i, file in enumerate(pdfs):
    print(f"{i}: '{pdfs[i]}'")

index = 0 if len(pdfs) == 1 else int(input(f"Which file do you want to simplify? (0-{len(pdfs) - 1}) > "))

start = input("At which page does the segment you want to simplify start? > ")

reader = PdfReader("pdf/example.pdf")
#
# print(len(reader.pages))
#
# # getting a specific page from the pdf file
# page = reader.pages[0]
#
# # extracting text from page
# text = page.extract_text()
# print(text)

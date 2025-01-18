from pypdf import PdfReader, PageObject
from os import listdir
from os.path import isfile, join


segmentation_options = ["sentence", "page"]


pdfs = [f for f in listdir("pdf") if isfile(join("pdf", f)) and f[-3:] == "pdf"]

if len(pdfs) == 0:
    print("Please put a pdf in the 'pdf' directory")
    exit()


for i, file in enumerate(pdfs):
    print(f"{i}: '{file}'")

index = 0 if len(pdfs) == 1 else int(input(f"Which file do you want to simplify? (0-{len(pdfs) - 1}) > "))


reader = PdfReader(f"pdf/{pdfs[index]}")


start = int(input(f"At which page does the segment you want to simplify start? (1-{len(reader.pages)}) > ")) - 1
end = int(input(f"At which page does the segment you want to simplify end? (1-{len(reader.pages)}) > ")) - 1


if end > len(reader.pages) or start > len(reader.pages) or start > end:
    print("Indexes aren't valid")
    exit()


for i, option in enumerate(segmentation_options):
    print(f"{i}: {option}")

option_index = int(input(f"How do you want to segment the pdf? (0-{len(segmentation_options) - 1}) > "))
option_count = int(input(f"Per how many {segmentation_options[option_index]}s do you want to cut the pdf? > "))


def get_full_text(start: int, end: int):
    output = ""
    for j in range(start, end + 1):
        output += reader.pages[j].extract_text()

    return output


def merge_list(l: list, count: int):
    if count == 1:
        return l
    l2 = []
    j = -1
    for i, element in enumerate(l):
        if i % count == 0:
            l2.append("")
            j += 1
        l2[j] += l[i] + "."
    return l2


def merge_list_reader(l: list[PageObject], count: int):
    if count == 1:
        return l
    l2 = []
    j = -1
    for i, element in enumerate(l):
        if i % count == 0:
            l2.append("")
            j += 1
        l2[j] += l[i].extract_text()
    return l2


def write_list_to_files(l: list):
    for i, element in enumerate(l):
        with open(f"segmented_output/segment{str(i)}.txt", "w", encoding="utf-8") as f:
            f.write(element)


match option_index:
    case 0: # sentence
        text = get_full_text(start, end)
        sentences = text.split(".")
        write_list_to_files(merge_list(sentences, option_count))

    case 1: # page
        write_list_to_files(merge_list_reader(reader.pages, option_count))


# json with info on ChatGPT API keys and stuff, make it input when first time,
# when not first time, ask if same info as last time (reuse code from ParcelsTracker)




# Thank you to user Greenstick for this code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

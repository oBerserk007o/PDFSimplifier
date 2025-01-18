from pypdf import PdfReader


def check_pdfs_dir():
    if len(pdfs) == 0:
        print("Please put a pdf in the 'pdf' directory")
        exit()


def check_key():
    with open("key.txt", "r") as f:
        if len(f.read().strip(" ")) == 0:
            print("Please put your key in the 'key.txt' file (If you don't have one, go to "
              "'https://platform.openai.com/settings/organization/api-keys' and put a little money on it (5$ should be plenty))")
            exit()


def list_pdfs(pdfs: list[str]):
    for i, file in enumerate(pdfs):
        print(f"{i}: '{file}'")


def choose_pdf_index(pdfs: list[str]) -> int:
    list_pdfs(pdfs)
    if len(pdfs) == 1:
        index = 0
    else:
        index = int(input(f"Which file do you want to simplify? (0-{len(pdfs) - 1}) > "))
    return index


def list_segmentation_options(segmentation_options: list[str]):
    for i, option in enumerate(segmentation_options):
        print(f"{i}: {option}")


def choose_segmentation_index(segmentation_options: list[str]) -> list[int]:
    list_segmentation_options(segmentation_options)
    segmentation_index = int(input(f"How do you want to segment the pdf (every 3 sentences works very well)? (0-{len(segmentation_options) - 1}) > "))
    count = int(input(f"Per how many {segmentation_options[segmentation_index]}s do you want to cut the pdf? > "))
    return [segmentation_index, count]


def choose_start_end_indexes(reader: PdfReader) -> list[int]:
    start = int(input(f"At which page does the segment you want to simplify start? (1-{len(reader.pages)}) > ")) - 1
    end = int(input(f"At which page does the segment you want to simplify end? (1-{len(reader.pages)}) > ")) - 1

    if end > len(reader.pages) or start > len(reader.pages) or start > end:
        print("Indexes aren't valid")
        exit()

    return [start, end]


# Thank you to user Greenstick for this code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def get_full_text(start: int, end: int, reader: PdfReader):
    output = ""
    print("Reading")
    for j in range(start, end + 1):
        output += reader.pages[j].extract_text()
        print_progress_bar(j - start, end - start)
    return output


def merge_list_elements_per_count(list_to_merge: list, count: int, is_reader: bool):
    # this function takes elements from a list and combines {count} of them into a new element in another list
    if count == 1:
        if is_reader:
            return [t.extract_text() for t in list_to_merge]
        return list_to_merge

    output_list = []
    j = -1
    for i, element in enumerate(list_to_merge):
        if i % count == 0:
            output_list.append("")
            j += 1

        if is_reader:
            output_list[j] += list_to_merge[i].extract_text()
        else:
            output_list[j] += list_to_merge[i] + "."
    return output_list


def write_list_to_files(list_to_write: list):
    print("Writing")
    for i, element in enumerate(list_to_write):
        with open(f"segmented_output/segment{str(i)}.txt", "w", encoding="utf-8") as f:
            f.write(element)
        print_progress_bar(i, len(list_to_write) - 1)
    print()


def main_segmenter(segmentation_index: int, count: int, start: int, end: int, reader: PdfReader):
    match segmentation_index:
        case 0: # sentence
            text = get_full_text(start, end, reader)
            sentences = text.split(".")
            merged_list = merge_list_elements_per_count(sentences, count, False)
            write_list_to_files(merged_list)

        case 1: # page
            merged_list = merge_list_elements_per_count(reader.pages, count, True)
            write_list_to_files(merged_list)

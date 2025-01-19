import time

from pypdf import PdfReader
from checks import smart_input
import logging


class Segmenter:
    def __init__(self, logger: logging):
        self.logger = logger


    def list_pdfs(self, pdfs: list[str]):
        for i, file in enumerate(pdfs):
            print(f"{i}: '{file}'")


    def choose_pdf_index(self, pdfs: list[str]) -> int:
        self.logger.debug("Choosing pdf file")
        self.list_pdfs(pdfs)
        if len(pdfs) == 1:
            index = 0
        else:
            index = smart_input(f"Which file do you want to simplify? (0-{len(pdfs) - 1}) > ")
        self.logger.debug(f"Chose pdf file '{pdfs[index]}'")
        return index


    def list_segmentation_options(self, segmentation_options: list[str]):
        for i, option in enumerate(segmentation_options):
            print(f"{i}: {option}")


    def choose_segmentation_index(self, segmentation_options: list[str]) -> list[int]:
        self.logger.debug("Choosing segmentation index and count")
        self.list_segmentation_options(segmentation_options)
        segmentation_index = smart_input(f"How do you want to segment the pdf (every 3 sentences usually works well, but it depends on your pdf)? (0-{len(segmentation_options) - 1}) > ")
        count = smart_input(f"Per how many {segmentation_options[segmentation_index]}s do you want to cut the pdf? > ")
        self.logger.debug(f"Chose segmentation index and count: {segmentation_options[segmentation_index]}, {count}")
        return [segmentation_index, count]


    def choose_start_end_indexes(self, reader: PdfReader) -> list[int]:
        self.logger.debug("Choosing start and end index")
        start = smart_input(f"At which page does the segment you want to simplify start? (1-{len(reader.pages)}) > ") - 1
        end = smart_input(f"At which page does the segment you want to simplify end? (1-{len(reader.pages)}) > ") - 1

        if end > len(reader.pages) or start > len(reader.pages) or start > end:
            print("Indexes aren't valid")
            self.logger.debug("Indexes invalid, exiting")
            exit()

        self.logger.debug(f"Chose start and end index: {start}, {end}")
        return [start, end]


    # Thank you to user Greenstick for this code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    def print_progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()


    def get_full_text(self, start: int, end: int, reader: PdfReader):
        self.logger.info("Reading full text")
        output = ""
        print("Reading")
        time1 = time.time()
        for j in range(start, end + 1):
            output += reader.pages[j].extract_text()
            self.print_progress_bar(j - start, end - start)
        time_taken = time.time() - time1
        print(f"Took {time_taken}s")
        self.logger.debug(f"Took {time_taken}s")
        self.logger.info("Read full text")
        return output


    def merge_list_elements_per_count(self, list_to_merge: list, count: int, is_reader: bool):
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


    def write_list_to_files(self, list_to_write: list):
        self.logger.info("Writing list to files")
        print("Writing")
        time1 = time.time()
        for i, element in enumerate(list_to_write):
            self.logger.debug(f"Writing {i}th element to file")
            with open(f"segmented_output/segment{str(i)}.txt", "w", encoding="utf-8") as f:
                f.write(element)
            self.print_progress_bar(i, len(list_to_write) - 1)
        time_taken = time.time() - time1
        print(f"Took {time_taken}s")
        self.logger.debug(f"Took {time_taken}s")
        self.logger.info("Wrote list to files")
        print()


    def main_segmenter(self, segmentation_index: int, count: int, start: int, end: int, reader: PdfReader):
        self.logger.info("Starting main segmenter")
        match segmentation_index:
            case 0: # sentence
                text = self.get_full_text(start, end, reader)
                sentences = text.split(".")
                merged_list = self.merge_list_elements_per_count(sentences, count, False)
                self.write_list_to_files(merged_list)

            case 1: # page
                merged_list = self.merge_list_elements_per_count(reader.pages, count, True)
                self.write_list_to_files(merged_list)
        self.logger.info("Main segmenter finished")

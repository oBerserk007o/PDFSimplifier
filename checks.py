#!/usr/bin/env python3
# coding: utf8

import os
import sys
from os import listdir
from os.path import isfile, join
import logging


def check_dirs(files_dirs: dict):
    dirs = listdir()
    for file_dir, should_be_empty in files_dirs.items():
        if isfile(file_dir):
            type = "File"
        else:
            type = "Directory"

        if file_dir not in dirs:
            if "." in file_dir:
                type = "File"
            else:
                type = "Directory"
            logging.error(f"{type} '{file_dir}' is missing, creating it")
            if type == "Directory":
                os.mkdir(file_dir)
            else:
                with open(file_dir, "x"):
                    pass

        if type == "Directory":
            if (len(listdir(file_dir)) == 0) and should_be_empty == "no":
                print(f"Directory '{file_dir}' is empty, put in the required elements")
                logging.error(f"Directory '{file_dir}' is empty")
                sys.exit()
            if (len(listdir(file_dir)) != 0) and should_be_empty == "yes":
                print(f"Directory '{file_dir}' isn't empty, please empty it")
                logging.error(f"Directory '{file_dir}' isn't empty")
                sys.exit()


def check_key():
    if "key.txt" not in listdir():
        with open("key.txt", "x"): pass

        print("Please add the API key inside the 'key.txt' file \n(here's how to make an API key: https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/)")
        logging.error("File 'key.txt' is missing")
        sys.exit()

    with open("key.txt", "r") as f:
        key = f.read()
        if len(key.strip(" ")) == 0:
            logging.error("Key is empty")
            print("Please put your key in the 'key.txt' file. If you don't have one, go to "
              "'https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/' and put a little money on it (5$ should be plenty for most cases)")
            sys.exit()
        if "\n" in key:
            logging.error("Key contains line breaks")
            print("Please put your key in the 'key.txt' file without any spaces or line breaks")


def smart_input(prompt: str, max_num: int, min_num: int = 0, retry_prompt: str = "Please enter a valid number"):
    result = input(prompt).strip(" ")
    while not result.isdigit() or not max_num >= int(result) >= min_num:
        print(retry_prompt)
        result = input(prompt)
    return int(result)


def confirm_settings(settings: dict):
    for setting, value in settings.items():
        print(f"{setting}: {value}")
    return not "n" in input("Do you confirm these settings? (Y/n) > ").lower()

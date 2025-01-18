from os import listdir
from os.path import isfile, join


def check_dirs(files_dirs: dict):
    dirs = listdir()
    for file_dir, should_be_empty in files_dirs.items():
        if isfile(join("./", file_dir)):
            type = "File"
        else:
            type = "Directory"

        if file_dir not in dirs:
            print(f"{type} '{file_dir}' is missing")
            exit()

        if type == "Directory":
            if (len(listdir(file_dir)) == 0) and should_be_empty == "no":
                print(f"Directory '{file_dir}' is empty, put in the required elements")
                exit()
            if (len(listdir(file_dir)) != 0) and should_be_empty == "yes":
                print(f"Directory '{file_dir}' isn't empty, please empty it")
                exit()


def check_key():
    if "key.txt" not in listdir():
        print("File 'key.txt' is missing, please add it with the API key inside \n(here's how to make an API key: https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/)")
        exit()

    with open("key.txt", "r") as f:
        key = f.read()
        if len(key.strip(" ")) == 0:
            print("Please put your key in the 'key.txt' file. If you don't have one, go to "
              "'https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/' and put a little money on it (5$ should be plenty for most cases)")
            exit()
        if "\n" in key:
            print("Please put your key in the 'key.txt' file without any spaces or line breaks")



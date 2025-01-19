import time
from os import listdir
from os.path import isfile, join
from openai import OpenAI, AuthenticationError
from checks import smart_input
import tiktoken
import logging


models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
# https://openai.com/api/pricing/
cost_per_token_per_model = {
    "gpt-4o-mini": 0.15,
    "gpt-4o": 2.5,
    "gpt-3.5-turbo": 3,
    "gpt-4-turbo": 10,
    "gpt-4": 30
}
languages = ["french", "english"]
context_messages = {
    "french": ["Peux-tu me réécrire ce texte en de plus simples termes?", "Donne-moi simplement le texte simplifié, sans autres mots."],
    "english": ["Can you simplify me this text into easier terms?", "Give me just the simplified text, without any other words"]
}

class Simplifier:
    def __init__(self, logger: logging):
        self.logger = logger


    def choose_language(self):
        self.logger.debug("Choosing language")
        for i, l in enumerate(languages):
            print(f"{i}: {l}")
        index = smart_input(f"In which language is the text? (0-{len(languages) - 1}) > ")
        self.logger.debug(f"Chose language {languages[index]}")
        return languages[index]


    def get_key(self):
        self.logger.debug("Reading key")
        with open("key.txt", "r", encoding="UTF-8") as fi:
            key = fi.read()

        if key != "":
            return key
        print("Please enter your key in the 'key.txt' file (If you don't have one, go to "
              "'https://platform.openai.com/settings/organization/api-keys' and put a little money on it (5$ should be plenty))")
        self.logger.debug("Key is empty, exiting")
        exit()


    # Thank you to user Greenstick for this code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
    def print_progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()


    def load_segments(self) -> list[str]:
        self.logger.info("Loading segments")
        files = [f for f in listdir("segmented_output") if isfile(join("segmented_output", f)) and f[-3:] == "txt"]
        if len(files) == 0:
            print("It seems the 'segmented_output' directory does not contain any text files, please run the segmenter first")
            self.logger.debug("'segmented_output' directory does not contain any text files, exiting")
            exit()

        segments = []
        for i, file in enumerate(files):
            with open("segmented_output/" + file, "r", encoding="utf-8") as f:
                segments.append(f.read())
        self.logger.info("Loaded segments")
        return segments


    def num_tokens_from_string(self, string: str, model_name: str) -> int:
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens


    def get_estimated_cost(self, segments: list, model_name: str, lang: str) -> float:
        tokens = 0
        for segment in segments:
            tokens += self.num_tokens_from_string(segment, model_name)

        tokens += len(segments) * self.num_tokens_from_string("".join([text for text in context_messages[lang]]), model_name)

        #       one million ↴
        cost = (tokens / 1000000) * cost_per_token_per_model[model_name]
        return cost


    def get_estimated_costs(self, segments: list, lang: str) -> list[float]:
        self.logger.debug("Estimating costs")
        costs = []
        print("Estimating costs")
        time1 = time.time()
        for i, model in enumerate(models):
            self.print_progress_bar(i, len(models) - 1)
            costs.append(round(self.get_estimated_cost(segments, model, lang), 4)*2)
        time_taken = time.time() - time1
        print(f"Took {time_taken}s")
        self.logger.debug(f"Took {time_taken}s")
        self.logger.debug("Estimated costs")
        return costs


    def list_models(self, segments: list, lang: str):
        costs = self.get_estimated_costs(segments, lang)
        for i, model in enumerate(models):
            print(f"{i}: '{model}', estimated cost: US${costs[i]}")
        print("*DISCLAIMER* The costs are approximate, and can be very far off the actual price, this is just to give you an idea\n")
        print("'gpt-4o-mini' is recommended, as it does the job well, and it's not too expensive\n")


    def choose_model(self, segments: list, lang: str) -> str:
        self.logger.debug("Choosing model")
        self.list_models(segments, lang)
        index = smart_input(f"Which model do you want to use? (0-{len(models) - 1}) > ")
        self.logger.debug(f"Chose model {models[index]}")
        return models[index]


    def mainloop_simplifier(self, segments: list, model: str, lang: str):
        self.logger.info("Starting main simplifier")
        client = OpenAI(api_key=self.get_key())
        print("\nSimplifying text\n")
        time1 = time.time()
        for i, segment in enumerate(segments):
            self.logger.debug(f"Sending {i}th request to ChatGPT")
            content_message = f'{context_messages[lang][0]} "{segment}" {context_messages[lang][1]}'

            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        # {"role": "system", "content": "You are a helpful assistant."},
                        {
                            "role": "user",
                            "content": content_message
                        }
                    ]
                )
            except AuthenticationError:
                print("Invalid API key, please follow this guide to make one: https://www.analyticsvidhya.com/blog/2024/10/openai-api-key-and-add-credits/")
                self.logger.critical("Invalid API key, exiting")
                exit()

            self.logger.debug("Received response from ChatGPT")
            simplified_segment = completion.choices[0].message.content

            with open(f"result/simplified_segment{i}.txt", "w", encoding="UTF-8") as f:
                f.write(simplified_segment)

            self.print_progress_bar(i, len(segments) - 1)
            self.logger.debug(f"Wrote response to file 'result/simplified_segment{i}.txt'")
        time_taken = time.time() - time1
        print(f"Took {time_taken}s")
        self.logger.debug(f"Took {time_taken}s")
        self.logger.info("Main simplifier finished")


    def compile_texts(self, model: str):
        self.logger.info("Compiling texts")
        print("Compiling texts")
        files = [f for f in listdir("result") if isfile(join("result", f)) and f[-3:] == "txt"]
        if len(files) == 0:
            print("It seems the 'result' directory does not contain any text files, there has been an error somewhere")
            self.logger.debug("'result' directory does not contain any text files, something went wrong")
            exit()
        text = ""
        for file in files:
            with open("result/" + file, "r", encoding="UTF-8") as f:
                text += f.read()

        text_to_write = "".join([line+".\n" for line in text.split(".")])

        time1 = time.strftime('%Y%m%d_%H%M%S')

        with open(f"simplified_text{time1}-{model}.txt", "w", encoding="UTF-8") as f:
            f.write(text_to_write)

        print(f"The simplified text is in 'simplified_text{time1}-{model}.txt'")
        print(f"Please move it to another directory, since it may get erased or cause errors if you run the program again")
        self.logger.info("Done compiling texts")

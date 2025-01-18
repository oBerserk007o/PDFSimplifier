from os import listdir
from os.path import isfile, join
from openai import OpenAI
import tiktoken

# choose language (done)
# read all segments and load them into list (done)
# loop through list to get estimates (done)
# progress bar (done)
# list models: "{i}: '{model}', estimated cost: {cost}" (done)
# choose model (done)
# send to ChatGPT
# progress bar
# receive responses and compile them into .txt file

models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
# https://openai.com/api/pricing/
cost_per_token_per_model = {
    "gpt-4o-mini": 0.15,
    "gpt-4o": 2.5,
    "gpt-3.5-turbo": 3,
    "gpt-4-turbo": 10,
    "gpt-4": 30
}
languages = ["fr", "en"]
lang = "en"
context_messages = {
    "fr": ["Peux-tu me réécrire ce texte en de plus simples termes?", "Donne-moi simplement le texte simplifié, sans autres mots."],
    "en": ["Peux-tu simplifier ce texte en de plus simples mots?"]
}


def choose_language():
    global lang
    for i, l in enumerate(languages):
        print(f"{i}: {l}")
    index = int(input(f"In which language is the text? (0-{len(languages) - 1}) > "))
    lang = languages[index]


def get_key():
    with open("key.txt", "r") as fi:
        key = fi.read()

    if key != "":
        return key
    print("Please enter your key in the 'key.txt' file (If you don't have one, go to "
          "'https://platform.openai.com/settings/organization/api-keys' and put a little money on it (5$ should be plenty))")
    exit()


# Thank you to user Greenstick for this code: https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def load_segments():
    files = [f for f in listdir("segmented_output") if isfile(join("segmented_output", f)) and f[-3:] == "txt"]
    segments = []
    for i, file in enumerate(files):
        with open("segmented_output/" + file, "r", encoding="utf-8") as f:
            segments.append(f.read())
    return segments


def num_tokens_from_string(string: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_estimated_cost(segments: list, model_name: str) -> int:
    tokens = 0
    for segment in segments:
        tokens += num_tokens_from_string(segment, model_name)

    tokens += len(segments) * num_tokens_from_string("".join([text for text in context_messages[lang]]), model_name)

    #       one million ↴
    cost = (tokens / 1000000) * cost_per_token_per_model[model_name]
    return cost


def get_estimated_costs(segments: list):
    costs = []
    print("Estimating costs")
    for i, model in enumerate(models):
        print_progress_bar(i, len(models) - 1)
        costs.append(round(get_estimated_cost(segments, model), 4))
    print()
    return costs


def list_models(segments: list):
    costs = get_estimated_costs(segments)
    for i, model in enumerate(models):
        print(f"{i}: '{model}', estimated cost: US${costs[i]}")
    print("'gpt-4o-mini' is recommended, as it does the job, and it's not too expensive\n")


def choose_model(segments: list):
    list_models(segments)
    index = int(input(f"Which model do you want to use? (0-{len(models) - 1}) > "))
    return models[index]


text_segments = load_segments()
choose_language()
choose_model(text_segments)


client = OpenAI(api_key=get_key())

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        #{"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

for choice in completion.choices:
    print(choice.message.content)




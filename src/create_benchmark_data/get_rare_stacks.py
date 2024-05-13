from pathlib import Path
from create_benchmark_data.utils import get_csv_data, write_json
from bosyl.tools import get_bo_symbols
import json
from botok import WordTokenizer


wt = WordTokenizer()

rare_stacks = Path(f"./data/stacks/rare_stacks.txt").read_text(encoding='utf-8').split("\n")
stacks_info = {}


def get_rare_stack_list():
    rare_stacks = ""
    punct = ""
    stacks = json.loads(Path(f"./data/stacks/stacks.json").read_text())
    for stack, count in stacks.items():
        if count < 500:
            if is_punct(stack) == False:
                rare_stacks += stack + "\n"
            else:
                punct += stack + "\n"
    Path(f"./data/stacks/rare_stacks.txt").write_text(rare_stacks)
    Path(f"./data/stacks/punct.txt").write_text(punct)


def is_punct(stack):
    count = 0
    tokens = wt.tokenize(stack)
    if len(tokens) > 1:
        for token in tokens:
            if token.chunk_type == "PUNCT":
                count += 1
        if count >= 1:
            return True
        else:
            return False
    else:
        if tokens[0].chunk_type == "PUNCT":
            return True
        else:
            return False


def count_stacks(text):
    stacks = {}
    symbols = get_bo_symbols(text)
    for symbol in symbols:
        if len(symbol) > 1:
            if symbol in stacks.keys():
                num = stacks[symbol]
                stacks[symbol] = num + 1
            else:
                stacks[symbol] = 1    


def create_norbuketaka_stacks_info(csv_path):
    curr_dict = {}
    batch_id = csv_path.stem
    csv_data = get_csv_data(csv_path)
    for row in csv_data[1:]:
        image_name = row[1]
        text = row[3]
        image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{image_name}"
        symbols = get_bo_symbols(text)
        for symbol in symbols:
            if symbol in rare_stacks:
                curr_dict = {
                    "image_url": image_url,
                    "text" : text
                }
                if symbol not in stacks_info:
                    stacks_info[symbol] = [curr_dict]
                else:
                    stacks_info[symbol].append(curr_dict)
            curr_dict = {}


def get_the_norbuketaka_rare_stacks_info():
    csv_paths = list(Path(f"./data/csv/norbuketaka/annotations/").iterdir())
    for csv_path in csv_paths:
        create_norbuketaka_stacks_info(csv_path)
    write_json(stacks_info, "./data/rare_stack_info.json")


    


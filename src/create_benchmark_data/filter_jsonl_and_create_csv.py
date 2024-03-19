import jsonlines
from pathlib import Path
from utils import write_csv

style_dict = {
    0: "others",
    1: "Umen",
    2: "Uchan",
    3: "not_classified"
}


def create_csv(file_paths):
    for file in file_paths:
        filename = file.stem
        batch_name = filename.split("_")[1]
        ids = []
        csv_data = []
        if int(batch_name[5:]) <= 10:
            with jsonlines.open(file) as reader:
                for obj in reader:
                    if obj['answer'] == "accept":
                        image_name = f"{obj['id']}.jpg"
                        if image_name in ids:
                            continue
                        image_url = obj['image'].split("?")[0]
                        text = obj['user_input']
                        data = [image_name, image_url, text]
                        csv_data.append(data)
                        ids.append(image_name)
        else:
            with jsonlines.open(file) as reader:
                for obj in reader:
                    if obj['answer'] == "accept":
                        image_name = f"{obj['id']}.jpg"
                        if image_name in ids:
                            continue
                        image_url = obj['image'].split("?")[0]
                        text = obj['user_input']
                        style_id = obj['accept'][0] if len(obj['accept']) != 0 else 3 
                        choice = style_dict[style_id]
                        if choice != "Uchan":
                            continue
                        data = [image_name, image_url, text]
                        csv_data.append(data)
                        ids.append(image_name)
        csv_path = f"./data/csv/Monlam/transcript/{batch_name}.csv"                              
        write_csv(csv_data, csv_path)



if __name__ == "__main__":
    file_paths = list(Path("./data/jsonl/Monlam").iterdir())
    create_csv(file_paths)
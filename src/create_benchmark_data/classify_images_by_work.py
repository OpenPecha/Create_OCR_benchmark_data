from pathlib import Path
import csv
import random
import json
import subprocess
from utils import write_csv, get_csv_data, download_and_save_image

master_dict = {}


def add_to_master_dict(work_id, curr_dict):
    if work_id not in master_dict:
        master_dict[work_id] = [curr_dict]
    else:
        master_dict[work_id].append(curr_dict)

def classify_by_work(csv_data, batch_id):
    for row in csv_data[1:]:
        work_id = row[0].split("/")[0]
        curr_dict = {
            "row": row,
            "batch_id": batch_id,
        }
        add_to_master_dict(work_id, curr_dict)
        curr_dict = {}

def get_csv_data(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def segment_dict(master_dict, max_work_ids=10):
    segmented_dicts = []
    temp_dict = {}
    count = 0  # Counter to keep track of how many work_ids have been added to the temp_dict
    
    for work_id, work_data in master_dict.items():
        temp_dict[work_id] = work_data
        count += 1
        
        if count == max_work_ids or work_id == list(master_dict.keys())[-1]:
            segmented_dicts.append(temp_dict)
            temp_dict = {}
            count = 0
    return segmented_dicts


def get_sample_images_per_work(master_dict):
    sample_images = {}
    for work_id, work_data in master_dict.items():
        if len(work_data) < 10:
            continue
        sample_images[work_id] = random.sample(work_data, 5)
    return sample_images

def get_the_images(sample_images):
    for work_id, work_data in sample_images.items():
        save_dir = Path(f"./data/images/norbuketaka/{work_id}")
        save_dir.mkdir(parents=True, exist_ok=True)
        for work_info in work_data:
            image_name = work_info["row"][1]
            batch_id = work_info["batch_id"]
            image_url = f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{image_name}"
            save_path = save_dir / image_name
            download_and_save_image(image_url, save_path)


def get_stacks():
    stacks = ""
    list_of_essentials = Path(f"./tibetan_essentials.txt").read_text().split("\n")
    for essential in list_of_essentials:
        if len(essential) >= 2:
            stacks += essential + "\n"
    Path(f"./stacks.txt").write_text(stacks, encoding="utf-8")

def main():
    csv_paths = list(Path(f"./data/csv/norbuketaka/annotations").iterdir())
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        csv_data = get_csv_data(csv_path)
        classify_by_work(csv_data, batch_id)
    sample_images = get_sample_images_per_work(master_dict)
    get_the_images(sample_images)
    



if __name__ == "__main__":
    main()

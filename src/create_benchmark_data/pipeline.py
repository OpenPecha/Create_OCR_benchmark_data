from pathlib import Path
from utils import get_csv_data, write_csv, calculate_splits
import csv
import random
import json
import math
import subprocess
from classify_images_by_work import classify_by_work

def get_url_for_norbuketaka(image_name, batch_id):
    return f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{image_name}"


def distribute_the_images(master_dict):
    sample_images = {}
    for work_id, work_data in master_dict.items():
        total_images = len(work_data)
        shuffled_data = work_data[:]  # Create a copy to shuffle
        random.shuffle(shuffled_data)
        if total_images < 100:
            train_count, val_count, _ = calculate_splits(total_images)
            training_data = shuffled_data[:train_count]
            validation_data = shuffled_data[train_count:train_count + val_count]
            test_data = shuffled_data[train_count + val_count:]
            sample_images[work_id] = {
                "training": training_data,
                "validation": validation_data,
                "benchmark": test_data
            }
        else:
            remaining_images = total_images - 50
            train_count = math.floor(remaining_images / 2)
            validation_data = remaining_images - train_count
            sample_images[work_id] = {
                "training": shuffled_data[:train_count],
                "validation": shuffled_data[train_count:train_count + val_count],
                "benchmark": shuffled_data[train_count + val_count:]
            }

    return sample_images



def main():
    csv_paths = list(Path("./data/norbuketaka/").iterdir())
    master_dict = classify_by_work(csv_paths)



if __name__ == "__main__":
    main()

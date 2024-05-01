import csv
import math
import json
import requests

def read_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json(json_data, json_path):
    with open(json_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent=4)


def write_csv(data, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def download_and_save_image(image_url, save_path):
    if save_path.exists():
        return
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")


def get_csv_data(csv_file_path):
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


# def calculate_splits(n, train_pct=43.5, val_pct=43.5, test_pct=13):
#     """Calculate number of items for each dataset split."""
#     train_count = math.floor(n * train_pct / 100)
#     val_count = math.floor(n * val_pct / 100)
#     test_count = n - train_count - val_count
#     return train_count, val_count, test_count

def calculate_splits(n, val_pct=40):
    """Calculate number of items for each dataset split."""
    val_count = math.floor(n * val_pct / 100)
    train_count = n - val_count
    return train_count, val_count

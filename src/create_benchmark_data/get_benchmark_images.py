import csv
import math
import json
import random
from pathlib import Path
from utils import write_csv, get_csv_data, download_and_save_image, write_json

def get_url_for_norbuketaka(id, batch_id):
    return f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{id}"


def get_url_for_monlam(id, batch_id):
    return f"https://s3.amazonaws.com/monlam.ai.ocr/line_to_text/{batch_id}/{id}"


def get_images_from_csv(csv_file_path, type):
    benchmark_data = []
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    if type == "monlam" and int((csv_file_path.stem)[5:]) <= 10:
        number_of_images_to_sample = 500
    else:
        return None
    data_list = random.sample(data, number_of_images_to_sample)
    for data in data_list:
        id = data[0]
        batch_id = csv_file_path.stem
        if type == "monlam":
            image_url = get_url_for_monlam(id, batch_id)
        elif type == "norbuketaka":
            image_url = data[1]
        text = data[2]
        benchmark_data.append([id, image_url, text])
    return benchmark_data


def create_benchmark_csv(benchmark_dir, transcript_dir, type):
    for file in list(transcript_dir.iterdir()):
        filename = file.stem
        csv_data = get_images_from_csv(file, type)
        if csv_data is None:
            continue
        csv_path = f"{benchmark_dir}/{filename}.csv"
        write_csv(csv_data, csv_path)
        
def get_benchmark_images():
    monlam_benchmark_csv_paths = list(Path(f"./data/csv/Monlam/benchmark/").iterdir())
    for csv_path in monlam_benchmark_csv_paths:
        batch_id = csv_path.stem
        save_dir = Path(f"./data/images/Monlam/benchmark/{batch_id}")
        if save_dir.exists() == False:
            save_dir.mkdir(parents=True, exist_ok=True)
        csv_data = get_csv_data(csv_path)
        for data in csv_data:
            id = data[0]
            image_url = data[1]
            image_path = save_dir / id
            if image_path.exists():
                continue
            download_and_save_image(image_url, image_path)
    norbuketaka_benchmark_csv_paths = list(Path(f"./data/csv/Norbuketaka/benchmark/").iterdir())
    for csv_path in norbuketaka_benchmark_csv_paths:
        batch_id = csv_path.stem
        save_dir = Path(f"./data/images/Norbuketaka/benchmark/{batch_id}")
        if save_dir.exists() == False:
            save_dir.mkdir(parents=True, exist_ok=True)
        csv_data = get_csv_data(csv_path)
        for data in csv_data:
            id = data[0]
            image_url = data[1]
            image_path = save_dir / id
            download_and_save_image(image_url, image_path)

def calculate_splits(n, train_pct=43.5, val_pct=43.5, test_pct=13):
    """Calculate number of items for each dataset split."""
    train_count = math.floor(n * train_pct / 100)
    val_count = math.floor(n * val_pct / 100)
    # Ensure the test count compensates for any rounding off in training and validation counts
    test_count = n - train_count - val_count
    return train_count, val_count, test_count

def split_dataset(stack_dict):
    """Split dataset into training, validation, and benchmark datasets."""
    total_images = 0
    for stack, data in stack_dict.items():
        dataset_splits = {
        'training': [],
        'validation': [],
        'benchmark': []
    }
        number_of_images = len(data)
        total_images += number_of_images
        shuffled_data = data[:]  # Create a copy to shuffle
        random.shuffle(shuffled_data)
        train_count, val_count, _ = calculate_splits(number_of_images)
        training_data = shuffled_data[:train_count]
        validation_data = shuffled_data[train_count:train_count + val_count]
        test_data = shuffled_data[train_count + val_count:]
        dataset_splits['training'].extend(training_data)
        dataset_splits['validation'].extend(validation_data)
        dataset_splits['benchmark'].extend(test_data)
        write_json(dataset_splits, Path(f"./data/rare_stacks/{stack}.json"))
        print(f"total images: {total_images}")


def merge_all_benchmark_data():
    json_paths = list(Path(f"./data/rare_stacks/").iterdir())
    all_benchmark_data = {
        'training': [],
        'validation': [],
        'benchmark': []
    }
    for json_path in json_paths:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        all_benchmark_data['training'].extend(data['training'])
        all_benchmark_data['validation'].extend(data['validation'])
        all_benchmark_data['benchmark'].extend(data['benchmark'])
    print(f"Training: {len(all_benchmark_data['training'])}")
    print(f"Validation: {len(all_benchmark_data['validation'])}")
    print(f"Benchmark: {len(all_benchmark_data['benchmark'])}")
    print(f"Total in merge_data: {len(all_benchmark_data['training']) + len(all_benchmark_data['validation']) + len(all_benchmark_data['benchmark'])}")
    write_json(all_benchmark_data, Path(f"./data/rare_stacks/all_benchmark_data.json"))


def get_benchmark_data():
    stack_dict = json.loads(Path(f"./data/stacks/rare_stacks_info.json").read_text(encoding="utf-8"))
    split_dataset(stack_dict)
    merge_all_benchmark_data()


def main():
    get_benchmark_data()


if __name__ == "__main__":
    main()
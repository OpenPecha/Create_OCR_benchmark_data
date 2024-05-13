import json
import random
from pathlib import Path
from create_benchmark_data.utils import write_csv, get_csv_data, write_json, calculate_splits
        

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


def get_csv_excluding_rare_stacks_rows():
    rare_images = []
    rare_stacks_benchmark_data = json.loads(Path(f"./data/rare_stacks/all_benchmark_data.json").read_text(encoding="utf-8"))
    for _, list in rare_stacks_benchmark_data.items():
        for row in list:
            url = row['image_url']
            image_name = url.split("/")[-1]
            batch_id = url.split("/")[-2]
            rare_images.append(image_name)

    csv_paths = Path(f"./data/csv/Norbuketaka/annotations/").iterdir()
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        csv_data = get_csv_data(csv_path)
        for data in csv_data:
            id = data[1]
            if id in rare_images:
                csv_data.remove(data)
        write_csv(csv_data, f"./data/norbuketaka/{batch_id}.csv")


def main():
    get_csv_excluding_rare_stacks_rows()


if __name__ == "__main__":
    main()
from pathlib import Path
import csv
from create_benchmark_data.utils import write_csv, download_and_save_image
import random


def get_random_images(csv_data, batch_id):
    benchmark_data = []
    image_dir = Path(f"./data/Nyibum/benchmark/images/{batch_id}/")
    data_list = random.sample(csv_data, 100)
    for data in data_list:
        id = data[0]
        image_url = data[1]
        text = data[2]
        benchmark_data.append([id, image_url, text])
    write_csv(benchmark_data, f"./data/Nyibum/benchmark/csv/{batch_id}.csv")
    for data in benchmark_data:
        id = data[0]
        image_url = data[1]
        image_path = image_dir / id
        download_and_save_image(image_url, image_path)
    return benchmark_data


def get_csv_data(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def remove_random_images_from_csv(csv_data, random_images, batch_id):
    for random_image in random_images:
        csv_data.remove(random_image)
    image_dir = Path(f"./data/Nyibum/new/images/{batch_id}/")
    for data in csv_data:
            id = data[0]
            image_url = data[1]
            image_path = image_dir / id
            download_and_save_image(image_url, image_path)
    return csv_data


def main():
    csv_paths = list(Path(f"./data/Nyibum/annotations/csv/").iterdir())
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        if batch_id in ["batch22", "batch21", "batch20"]:
            csv_data = get_csv_data(csv_path)
            random_images = get_csv_data(f"./data/Nyibum/benchmark/csv/{batch_id}.csv")
            new_csv_data = remove_random_images_from_csv(csv_data[1:], random_images, batch_id)
            write_csv(new_csv_data, f"./data/Nyibum/new/csv/{batch_id}.csv")
        else:
            csv_data = get_csv_data(csv_path)
            random_images = get_random_images(csv_data[1:], batch_id)
            new_csv_data = remove_random_images_from_csv(csv_data[1:], random_images, batch_id)
            write_csv(new_csv_data, f"./data/Nyibum/new/csv/{batch_id}.csv")


if __name__ == "__main__":
    main()
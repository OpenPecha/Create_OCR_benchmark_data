import random
import math
import subprocess
from pathlib import Path
from create_benchmark_data.utils import calculate_splits, write_json, read_json, write_csv
from create_benchmark_data.classify_images_by_work import classify_by_work

def get_url_for_norbuketaka(image_name, batch_id):
    return f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{image_name}"


def distribute_the_images(master_dict):
    all_training_data = {
        'training': []
        }
    all_validation_data = {
        'validation': []
    }
    all_test_data = {
        'benchmark': []
    }
    distributed_images = {}
    for work_id, work_data in master_dict.items():
        total_images = len(work_data)
        shuffled_data = work_data[:]  # Create a copy to shuffle
        random.shuffle(shuffled_data)
        if total_images < 10:
            print(f"Work ID: {work_id} has less than 10 images. Skipping this work.")
            continue
        elif total_images < 100:
            train_count, val_count, _ = calculate_splits(total_images)
            training_data = shuffled_data[:train_count]
            validation_data = shuffled_data[train_count:train_count + val_count]
            test_data = shuffled_data[train_count + val_count:]
            distributed_images[work_id] = {
                "training": training_data,
                "validation": validation_data,
                "benchmark": test_data
            }
        else:
            remaining_images = total_images - 50
            train_count = math.floor(remaining_images / 2)
            val_count = remaining_images - train_count
            training_data = shuffled_data[:train_count]
            validation_data = shuffled_data[train_count:train_count + val_count]
            test_data = shuffled_data[train_count + val_count:]
            distributed_images[work_id] = {
                "training": training_data,
                "validation": validation_data,
                "benchmark": test_data
            }
        all_training_data['training'].extend(training_data)
        all_validation_data['validation'].extend(validation_data)
        all_test_data['benchmark'].extend(test_data)
    return distributed_images, all_training_data, all_validation_data, all_test_data

def create_distributed_jsons(rare_images):
    csv_paths = list(Path("./data/norbuketaka/").iterdir())
    master_dict = classify_by_work(csv_paths, rare_images)
    # master_dict = read_json(Path("./master.json"))
    distributed_images, all_training, all_validation_data, all_test_data = distribute_the_images(master_dict)
    write_json(distributed_images, Path(f"./distributed_images.json"))
    write_json(all_training, f"./all_training.json")
    write_json(all_validation_data, f"./all_validation.json")
    write_json(all_test_data, f"./all_test.json")


def get_benchmark_images_and_create_csv():
    desired_csv = []
    json_data = read_json(Path(f"./all_test.json"))['benchmark']
    for data in json_data:
        text = data['row'][3]
        image_name = data['row'][1]
        batch_id = data['batch_id']
        image_path = Path(f"/Users/tashitsering/Desktop/Norbuketaka/images/{batch_id}/{image_name}")
        save_path = Path(f"./data/benchmark/others/{image_name}")
        subprocess.run(["cp", str(image_path), str(save_path)])
        new_line = [image_name,text]
        desired_csv.append(new_line)
    write_csv(desired_csv, f"./data/benchmark/test.csv")

def seperate_data(data_list, rare_stacks):
    num = 0
    batch_name = 1
    desired_csv = []
    lines_per_batch = 100000
    for data in data_list:
        text = data['row'][3]
        image_name = data['row'][1]
        if image_name in rare_stacks:
            continue
        batch_id = data['batch_id']
        image_path = Path(f"/Users/tashitsering/Desktop/Norbuketaka/images/{batch_id}/{image_name}")
        save_dir = Path(f"./data/validation/batch_{batch_name}/")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = Path(save_dir/f"{image_name}")
        subprocess.run(["cp", str(image_path), str(save_path)])
        new_line = [image_name,text]
        desired_csv.append(new_line)
        num += 1

        if num == lines_per_batch:
            write_csv(desired_csv, f"./csv/validation_{batch_name}.csv")
            desired_csv = []
            num = 0
            batch_name += 1

    if desired_csv:
        write_csv(desired_csv, f"./csv/validation_{batch_name}.csv")

def seperate_all_rare_case_data(data):
    training_data = data["training"]
    validation_data = data["validation"]
    training_csv = []
    for data in training_data:
        text = data['text']
        url_data = data['image_url'].split("/")
        image_name = url_data[7]
        batch_id = url_data[6]
        image_path = Path(f"/Users/tashitsering/Desktop/Norbuketaka/images/{batch_id}/{image_name}")
        save_dir = Path(f"./data/training/batch_20/")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = Path(save_dir/f"{image_name}")
        subprocess.run(["cp", str(image_path), str(save_path)])
        new_line = [image_name,text]
        training_csv.append(new_line)
    write_csv(training_csv, f"./csv/training_20.csv")

    for data in validation_data:
        text = data['text']
        url_data = data['image_url'].split("/")
        image_name = url_data[7]
        batch_id = url_data[6]
        image_path = Path(f"/Users/tashitsering/Desktop/Norbuketaka/images/{batch_id}/{image_name}")
        save_dir = Path(f"./data/validation/batch_20/")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = Path(save_dir/f"{image_name}")
        subprocess.run(["cp", str(image_path), str(save_path)])
        new_line = [image_name,text]
        training_csv.append(new_line)
    write_csv(training_csv, f"./csv/validation_20.csv")

def create_benchmark_csv(rare_case_data):
    benchmark_csv = []
    benchmark_data = rare_case_data["benchmark"]
    for data in benchmark_data:
        text = data['text']
        url_data = data['image_url'].split("/")
        image_name = url_data[7]
        batch_id = url_data[6]
        image_path = Path(f"/Users/tashitsering/Desktop/Norbuketaka/images/{batch_id}/{image_name}")
        save_dir = Path(f"./data/benchmark/rare_stacks/")
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = Path(save_dir/f"{image_name}")
        new_line = [image_name,text]
        benchmark_csv.append(new_line)
        if save_path.exists:
            continue
        else:
            subprocess.run(["cp", str(image_path), str(save_path)])
    write_csv(benchmark_csv, f"./data/benchmark/rare_stacks.csv")

def put_transcript_with_images():
    training_batch_dir = Path(f"./data/validation/").iterdir()
    for training_batch in training_batch_dir:
        batch_num = training_batch.stem.split("_")[-1]
        if batch_num == "stacks": #or int(batch_num) <= 18
            continue
        csv_path = Path(f"./new_csv/validation_{batch_num}.csv")
        save_path = f"{training_batch}/transcripts.csv"
        subprocess.run(["cp", str(csv_path), str(save_path)])


def main():
    put_transcript_with_images()
    # rare_images = Path(f"./data/rare_images.txt").read_text(encoding='utf-8').splitlines()
    # create_new_validation_set(rare_images)
    # create_distributed_jsons(rare_images)
    # rare_case_data = read_json(Path(f"./data/rare_stacks/all_benchmark_data.json"))
    # create_benchmark_csv(rare_case_data)
    # seperate_all_rare_case_data(rare_case_data)

    


if __name__ == "__main__":
    main()

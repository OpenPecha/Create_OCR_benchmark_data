import csv
import random
from pathlib import Path
from utils import write_csv



def get_ten_percent_images_from_csv(csv_file_path):
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    ten_percent = int(len(data) * 0.1)
    images = random.sample(data, ten_percent)
    return images

def create_benchmark_csv(benchmark_dir, transcript_dir):
    for file in benchmark_dir.iterdir():
        if file.suffix == ".csv":
            images = get_ten_percent_images_from_csv(file)
            file_name = file.stem
            


def main():
    monlam_benchmark_dir = Path(f"./data/csv/Monlam/")
    monlam_transcript_dir = Path(f"./data/csv/Monlam/transcript/")
    norbuketaka_benchmark_dir = Path(f"./data/csv/Norbuketaka/benchmark/")
    norbuketaka_transcript_dir = Path(f"./data/csv/Norbuketaka/transcript/")
    create_benchmark_csv(monlam_benchmark_dir, monlam_transcript_dir)
    create_benchmark_csv(norbuketaka_benchmark_dir, norbuketaka_transcript_dir)
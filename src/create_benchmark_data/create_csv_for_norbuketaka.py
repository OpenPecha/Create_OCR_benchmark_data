import csv
from pathlib import Path
from create_benchmark_data.utils import write_csv


def get_url_for_norbuketaka(id, batch_id):
    return f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{id}"


def get_desired_data_format(file_path, batch_id):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
        desired_csv = []
        for line in data[1:]:
            id = line[1]
            image_url = get_url_for_norbuketaka(id, batch_id)
            text = line[3]
            new_line = [id,image_url,text]
            desired_csv.append(new_line)
    return desired_csv

def main():
    annotation_path = Path("./data/csv/norbuketaka/annotations").iterdir()
    for file_path in annotation_path:
        filename = file_path.stem
        data = get_desired_data_format(file_path, filename)
        write_csv(data, f"./data/csv/norbuketaka/transcript/{filename}.csv")
    

if __name__ == "__main__":
    main()
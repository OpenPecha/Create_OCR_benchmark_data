import csv

def write_csv(data, file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
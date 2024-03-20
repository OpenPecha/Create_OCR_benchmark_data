from pathlib import Path
from utils import get_csv_data


master_dict = {}


def add_to_master_dict(work_id, curr_dict):
    if work_id not in master_dict:
        master_dict[work_id] = [curr_dict]
    else:
        master_dict[work_id].append(curr_dict)


def classify_by_work(csv_paths):
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        csv_data = get_csv_data(csv_path)
        for row in csv_data[1:]:
            work_id = row[0].split("/")[0]
            curr_dict = {
                "row": row,
                "batch_id": batch_id,
            }
            add_to_master_dict(work_id, curr_dict)
            curr_dict = {}
    return master_dict


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
            

def get_stacks():
    stacks = ""
    list_of_essentials = Path(f"./tibetan_essentials.txt").read_text().split("\n")
    for essential in list_of_essentials:
        if len(essential) >= 2:
            stacks += essential + "\n"
    Path(f"./stacks.txt").write_text(stacks, encoding="utf-8")


def main():
    csv_paths = list(Path(f"./data/norbuketaka/").iterdir())
    master_dict = classify_by_work(csv_paths)
    return master_dict
    

if __name__ == "__main__":
    main()

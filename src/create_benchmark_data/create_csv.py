from pathlib import Path
from PIL import Image
from create_benchmark_data.utils import read_json, get_csv_data, write_csv, write_json


def get_print_method_of_work_ids():
    master = read_json(Path("./master.json"))
    keys = master.keys()
    with open('keys.txt', 'w') as file:
        for key in keys:
            file.write(f"{key}\n")
    for data in master:
        print(data)

def get_image_ids():
    image_ids = []
    paths = Path(f"./new_csv/").iterdir()
    for csv_path in paths:
        csv_data = get_csv_data(csv_path)
        for row in csv_data[1:]:
            image_id = row[0]
            image_ids.append(image_id)
    return image_ids


# def get_batch_info():
#     csv_paths = list(Path("./csv/").iterdir())
#     for csv_path in csv_paths:
#         csv_data = get_csv_data(csv_path)
#         for data in csv_data:
#             image_name = data[1]
            


def get_image_dict():
    curr = {}
    image_dict = {}
    image_ids = get_image_ids()
    work_info = read_json(Path(f"./work_info.json"))
    # batch_info = get_image_batch_id()
    csv_paths = list(Path(f"./data/csv/norbuketaka/annotations/").iterdir())
    for csv_path in csv_paths:
        batch_id = csv_path.stem
        csv_data = get_csv_data(csv_path)
        for training_data in csv_data[1:]:
            work_id = training_data[0].split("/")[0]
            filename = training_data[1]
            # if filename in image_ids:
            #     continue
            text = training_data[3]
            char_len = len(text)
            print_type = work_info[work_id]['printMethod'][0]
            script = work_info[work_id]['script'][0]
            # batch_id = training_data['batch_id']
            url = f"https://s3.amazonaws.com/monlam.ai.ocr/norbuketaka/images/{batch_id}/{filename}"
            curr[filename]=[filename,text,url,work_id,print_type,script,char_len]
            image_dict.update(curr)
            curr = {}
    write_json(image_dict, "./new_dict_with_meta_for_training_2.json")
    return image_dict


def get_image_dimension(image_path):
    with Image.open(image_path) as img:
        return img.size  # img.size is a tuple (width, height)



def creat_new_csv():
    # nre_row = []
    training_csv = []
    # image_dict = get_image_dict()
    image_dict = read_json(Path("./new_dict_with_meta_for_training_2.json"))
    csv_paths = list(Path(f"./csv/").iterdir())
    for csv_path in csv_paths:
        csv_name = csv_path.stem
        if csv_name.split("_")[0] == "training":
            continue
        training_csv.append(["filename","transcript","url","work_id","printMethod","script","char_len","image_dimension"])
        csv_data = get_csv_data(csv_path)
        for row in csv_data:
            image_name = row[0]
            try:
                new_row = image_dict[image_name]
                batch_num = csv_name.split("_")[-1]
                image_path = Path(f"./data/validation/batch_{batch_num}/{image_name}")
                dimensions = get_image_dimension(image_path)
                new_row.append(f"{dimensions[0]}x{dimensions[1]}")
                training_csv.append(new_row)
            except:
                break
        write_csv(training_csv, f"./new_csv/{csv_name}.csv")
        training_csv = []


if __name__ == "__main__":
    creat_new_csv()
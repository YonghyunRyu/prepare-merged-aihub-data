import json
import zipfile
import argparse
import pandas as pd
from pathlib import Path
from zipfile import ZipFile


class ParaReader:
    @staticmethod
    def get(tree, curr_path):
        para = []
        if isinstance(tree, list):
            print(curr_path)
            for filename in tree:
                file_path = curr_path / filename
                print(file_path)
                para += ParaReader.get_from_file(file_path)
                print(len(para))
        elif isinstance(tree, dict):
            for next_path in tree:
                if next_path.endswith(".zip"):
                    assert (curr_path / next_path).exists()
                    assert zipfile.is_zipfile((curr_path / next_path))
                    print(curr_path / next_path, tree[next_path])
                    para += ParaReader.get_in_zip(curr_path / next_path, tree[next_path])
                else:
                    print(curr_path / next_path)
                    para += ParaReader.get(tree[next_path], curr_path / next_path)
                print(len(para))
        return para

    @staticmethod
    def get_from_file(path):
        if path.suffix == ".xlsx":
            return ParaReader.get_from_excel(path)
        elif path.suffix == ".json":
            return ParaReader.get_from_json(path)
        return []

    @staticmethod
    def read_excel(io):
        dataframe = pd.read_excel(io, engine="openpyxl")
        return dataframe

    @staticmethod
    def get_from_excel(io):
        dataframe = ParaReader.read_excel(io)
        para = ParaReader.get_from_dataframe(dataframe)
        return para

    @staticmethod
    def get_from_dataframe(dataframe):
        para = []
        for index, row in dataframe.iterrows():
            ko = row['원문']
            en = row['번역문']
            para.append({
                "ko": ko,
                "en": en
            })
        return para

    @staticmethod
    def get_from_json(io):
        para = []
        json_object = json.load(io)
        data = json_object
        if isinstance(data, dict):
            data = json_object["data"]

        for this_datum in data:
            key_of_ko = "ko"
            if "한국어" in this_datum:
                key_of_ko = "한국어"
            key_of_en = "en"
            if "영어" in this_datum:
                key_of_en = "영어"

            ko = this_datum[key_of_ko]
            en = this_datum[key_of_en]
            para.append({
                "ko": ko,
                "en": en
            })
        return para

    @staticmethod
    def get_from_zip(zip_file, filename):
        para = []
        with zip_file.open(filename) as f:
            if filename.endswith(".xlsx"):
                para += ParaReader.get_from_excel(f)
            elif filename.endswith(".json"):
                para += ParaReader.get_from_json(f)
        return para

    @staticmethod
    def get_in_zip(zip_path, filenames):
        para = []
        with ZipFile(zip_path) as zip_file:
            for this_name in zip_file.namelist():
                if this_name.encode("cp437").decode("cp949") not in filenames:
                    continue
                para += ParaReader.get_from_zip(zip_file, this_name)
                print(zip_path, this_name, len(para))
        return para


TRAIN_TREE = {
    "전문분야한영": {
        "Training/ko2en_training_json.zip": [
            'ko2en_edu_notice_1_training.json',
            'ko2en_finance_1_training.json',
            'ko2en_folk_and_food_1_training.json',
            'ko2en_it_and_tech_1_training.json',
            'ko2en_law_1_training.json',
            'ko2en_medical_1_training.json',
            'ko2en_sports_1_training.json',
            'ko2en_travel_1_training.json'
        ]
    },
    "한국어-영어 번역 말뭉치(기술과학)": {
        "Training/01_기술과학_ICT분야_학습데이터.zip": [
            "tech_train_set_700665.json"
        ]
    },
    "한국어-영어 번역 말뭉치(사회과학)": {
        "Training/02_사회과학_문화분야_학습데이터.zip": [
            "social_train_set_477967.json"
        ]
    },
    "한국어-영어 번역(병렬) 말뭉치": {
        ".": [
            "1_구어체(1).xlsx",
            "1_구어체(2).xlsx",
            "2_대화체.xlsx",
            "3_문어체_뉴스(2).xlsx",
            "3_문어체_뉴스(3).xlsx",
            "3_문어체_뉴스(4).xlsx",
            "4_문어체_한국문화.xlsx",
            "5_문어체_조례.xlsx",
            "6_문어체_지자체웹사이트.xlsx"
        ],
        "3_문어체_뉴스(1).zip": [
            "3_문어체_뉴스(1)_200226.xlsx"
        ]
    }
}

VALIDATION_TREE = {
    "전문분야한영": {
        "Validation/ko2en_validation_json.zip": [
            'ko2en_edu_notice_2_validation.json',
            'ko2en_finance_2_validation.json',
            'ko2en_folk_and_food_2_validation.json',
            'ko2en_it_and_tech_2_validation.json',
            'ko2en_law_2_validation.json',
            'ko2en_medical_2_validation.json',
            'ko2en_sports_2_validation.json',
            'ko2en_travel_2_validation.json'
        ]
    },
    "한국어-영어 번역 말뭉치(기술과학)": {
        "Validation/01_기술과학_ICT분야_검증데이터.zip": [
            "tech_valid_set_87583.json"
        ]
    },
    "한국어-영어 번역 말뭉치(사회과학)": {
        "Validation/02_사회과학_문화분야_검증데이터.zip": [
            "social_valid_set_59746.json"
        ]
    }
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='prepare merged aihub parallel data.')
    parser.add_argument('--data-dir')
    parser.add_argument('--output-dir', default='.')
    parser.add_argument('--valid', action='store_true')
    args = parser.parse_args()
    data_dir = args.data_dir
    output_dir = args.output_dir
    is_valid = args.valid

    data_dir_path = Path(data_dir)
    output_dir = Path(output_dir)
    data_tree = TRAIN_TREE
    split_name = 'train'
    if is_valid:
        data_tree = VALIDATION_TREE
        split_name = 'valid'
    corpus = ParaReader.get(data_tree, data_dir_path)

    ko_path = output_dir / f"{split_name}.ko"
    en_path = output_dir / f"{split_name}.en"

    with open(ko_path, "w", encoding="utf-8") as f_ko, \
            open(en_path, "w", encoding="utf-8") as f_en:
        for pair in corpus:
            ko = pair["ko"].strip()
            en = pair["en"].strip()
            f_ko.write(f'{ko}\n')
            f_en.write(f'{en}\n')

    print(f"{len(corpus)} pairs saved on {ko_path} and {en_path}")

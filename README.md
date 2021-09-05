# Prepare merged AIHub data

## Quickstart
### Parallel corpus
```
# download data from `https://aihub.or.kr/` 
pip install -r requirements.txt
python prepare-merged-aihub-parallel-data.py --data-dir <data_dir>
```

## Requirements
### python packages
```
pip install -r requirments.txt
```
### Data
download from `https://aihub.or.kr/`
#### parallel corpus
- `한국어-영어 번역 말뭉치(사회과학)`
- `한국어-영어 번역 말뭉치(기술과학)`
- `한국어-영어 번역(병렬) 말뭉치`
- `전문분야한영`

Then the structure of the `data_dir` should be as below
```
<data_dir>
├── 한국어-영어 번역 말뭉치(사회과학)
│   ├── Training
│   │   └── 02_사회과학_문화분야_학습데이터.zip
│   └── Validation
│       └── 02_사회과학_문화분야_검증데이터.zip
├── 한국어-영어 번역 말뭉치(기술과학)
│   ├── Training
│   │   └── 01_기술과학_ICT분야_학습데이터.zip
│   └── Validation
│       └── 01_기술과학_ICT분야_검증데이터.zip
├── 한국어-영어 번역(병렬) 말뭉치
│   ├── 1_구어체(1).xlsx
│   ├── 1_구어체(2).xlsx
│   ├── 2_대화체.xlsx
│   ├── 3_문어체_뉴스(1).zip
│   ├── 3_문어체_뉴스(2).xlsx
│   ├── 3_문어체_뉴스(3).xlsx
│   ├── 3_문어체_뉴스(4).xlsx
│   ├── 4_문어체_한국문화.xlsx
│   ├── 5_문어체_조례.xlsx
│   └── 6_문어체_지자체웹사이트.xlsx
└── 전문분야한영
    ├── Training
    │   ├── ko2en_training_csv.zip
    │   └── ko2en_training_json.zip
    └── Validation
        ├── ko2en_validation_csv.zip
        └── ko2en_validation_json.zip
```
Note: you don't need to unzip or change names.

# training/data/build_ner_dataset.py
from utils_data import fetch_data_from_mongo, convert_to_bio, split_train_valid, save_ner_tuples_to_jsonl
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    col = fetch_data_from_mongo(
        mongo_uri=os.getenv("MONGO_URI"),
        db_name="label-studio",
        collection="ner-labeled-output",
    )
    
    cursor= col.find({})
    tasks = cursor.to_list()

    bio_samples = convert_to_bio(tasks)
    train_set, valid_set = split_train_valid(bio_samples, valid_ratio=0.1)
    
    train_dataset = save_ner_tuples_to_jsonl(train_set, output_path="datasets/train_ner.jsonl")
    valid_dataset = save_ner_tuples_to_jsonl(valid_set, output_path="datasets/valid_ner.jsonl")
    
    return train_set, valid_set

if __name__ == "__main__":
    main()

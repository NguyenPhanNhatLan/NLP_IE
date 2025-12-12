import logging
import re
import os
import json
from typing import Any, Dict, List, Tuple
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, InvalidName
from sklearn.model_selection import train_test_split


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def fetch_data_from_mongo(mongo_uri: str, collection: str, db_name: str):
    logging.info(f"Input params: mongo_uri={mongo_uri}, db={db_name}, collection={collection}")
    try:
        client = MongoClient(mongo_uri)
        logging.info("MongoClient created successfully.")

        db = client[db_name]
        logging.info(f"Database '{db_name}' accessed successfully.")
        
        col = db[collection]
        logging.info(f"Collection '{collection}' ready to use.")

        return col

    except ConfigurationError as e:
        logging.error(f"MongoDB Configuration Error: {e}")
    except ConnectionFailure as e:
        logging.error(f"Cannot connect to MongoDB server: {e}")
    except InvalidName as e:
        logging.error(f"Invalid database or collection name: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

    logging.warning("Returning None due to previous errors.")
    return None

def convert_to_bio(tasks):
    bio_samples = []
    for task in tasks:
        text = task.get("data", {}).get("text")
        if not text:
            continue
        spans = _get_spans(task)
        tokens_with_tags = _find_bio_in_text(text, spans)
    
        if tokens_with_tags:
            bio_samples.append(tokens_with_tags)
            
    return bio_samples        
    
        

def _get_spans(task):
    annotation = task.get("annotations")[0].get('result')
    spans = []
    for anno in annotation:
        start = anno.get('value').get("start")
        end = anno.get('value').get("end")
        label = anno.get('value').get("labels") 
        if 'O' not in label:
            spans.append((start,end,label))
            
    return spans

def _find_bio_in_text(text, spans):
    tokens_w_tags = []
    for match in re.finditer(r"[^,;\s.]+", text):
        token = match.group()
        start_tok = match.start()
        end_tok = match.end()
        
        tag = 'O'
        
        for start, end, label in spans:
            if start_tok >= start and end_tok <= end+1:
                if start_tok== start:
                    tag = f'B-{label[0]}'
                else: 
                    tag = f'I-{label[0]}'
                continue
        
        tokens_w_tags.append((token, tag))
        
    return tokens_w_tags
        
    

def split_train_valid(
    bio_samples: List[Dict[str, Any]], 
    valid_ratio: float = 0.1,
    seed: int = 42
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not bio_samples:
        return [], []
    
    train_samples, valid_samples = train_test_split(
        bio_samples,
        test_size=valid_ratio,
        random_state=seed,
        shuffle=True
    )
    
    return train_samples, valid_samples



def save_ner_tuples_to_jsonl(data, output_path="dataset.jsonl"):
    with open(output_path, "w", encoding="utf-8") as f:
        for sentence in data:
            tokens = [tok for tok, label in sentence]
            labels = [label for tok, label in sentence]
            json.dump({"tokens": tokens, "labels": labels}, f, ensure_ascii=False)
            f.write("\n")

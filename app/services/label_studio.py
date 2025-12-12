from typing import List, Dict
import logging
from pymongo import InsertOne
from pymongo.errors import PyMongoError


def process_and_store_labeled_data(collection, docs: List[Dict]):
    try:
        if not docs:
            return {"inserted": 0}

        operations = []
        for d in docs:
            if "id" not in d:
                continue  
            operations.append(
                InsertOne(d)
            )

        if not operations:
            return {"inserted": 0}

        result = collection.bulk_write(
            operations,
            ordered=False 
        )

        return {
            "inserted": result.inserted_count
        }

    except PyMongoError as e:
        logging.error(f"Mongo insert error: {e}")
        raise RuntimeError("MongoDB insert failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")


def delete_all_labeled_data(collection):
    try:
        result = collection.delete_many({})
        return {
            "deleted": result.deleted_count
        }

    except PyMongoError as e:
        logging.error(f"Mongo delete error: {e}")
        raise RuntimeError("MongoDB delete failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")


def get_all_labeled_data(collection):
    try:
        docs = collection.find({}).to_list(length=None)
        return docs

    except PyMongoError as e:
        logging.error(f"Mongo fetch error: {e}")
        raise RuntimeError("MongoDB fetch failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")



def process_and_store_labeled_data(collection, docs: List[Dict]):
    try:
        if not docs:
            return {"inserted": 0}

        result = collection.insert_many(docs)
        return {
            "inserted": len(result.inserted_ids)
        }

    except PyMongoError as e:
        logging.error(f"Mongo insert error: {e}")
        raise RuntimeError("MongoDB insert failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")


def delete_all_labeled_data(collection):
    try:
        result = collection.delete_many({})
        return {
            "deleted": result.deleted_count
        }

    except PyMongoError as e:
        logging.error(f"Mongo delete error: {e}")
        raise RuntimeError("MongoDB delete failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")


def get_all_labeled_data(collection):
    try:
        docs = collection.find({}).to_list(length=None)
        return docs

    except PyMongoError as e:
        logging.error(f"Mongo fetch error: {e}")
        raise RuntimeError("MongoDB fetch failed")

    except Exception as e:
        logging.error(f"Service error: {e}")
        raise RuntimeError("Internal processing error")

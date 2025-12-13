from typing import List, Dict
import logging
from pymongo import InsertOne
from pymongo.errors import PyMongoError, BulkWriteError

def process_and_store_data(collection, docs: List[Dict]):
    try:
        if not docs:
            return {"inserted": 0}
    
        operations = [InsertOne(doc) for doc in docs if "id" in doc]
        
        if not operations:
            logging.warning("No valid documents to insert")
            return {"inserted": 0}
        
        result = collection.bulk_write(operations, ordered=False)
        return {"inserted": result.inserted_count}
        
    except BulkWriteError as e:
        inserted = e.details.get('nInserted', 0)
        logging.warning(f"Bulk insert partially failed. Inserted: {inserted}")
        return {"inserted": inserted}
        
    except PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
        raise RuntimeError("MongoDB operation failed")

def delete_by_ids(collection,  ids: List[str]):
    try:
        if not ids:
            return {"deleted": 0, "not_found": []}
        existing_docs = list(collection.find(
            {"id": {"$in": ids}},
            {"id": 1}
        ))
        
        existing_ids = [doc["id"] for doc in existing_docs]
        
        not_found_ids = [id for id in ids if id not in existing_ids]
        
        if existing_ids:
            result = collection.delete_many({"id": {"$in": existing_ids}})
            deleted_count = result.deleted_count
        else:
            deleted_count = 0
        
        return {
            "deleted": deleted_count,
            "not_found": not_found_ids
        }
        
    except PyMongoError as e:
        logging.error(f"MongoDB delete error: {e}")
        raise RuntimeError("MongoDB delete failed")
import json
import logging
import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.api.deps import get_db
from app.services.label_studio import (
    delete_by_ids,
    process_and_store_data,
)

router = APIRouter(
    tags=["RE labeled Data"]
)

COLLECTION_NAME = os.getenv("RE_LABELED_COLLECTION")
print(COLLECTION_NAME)
@router.post("/re/insert-all", status_code=status.HTTP_201_CREATED)
async def upload_json(file: UploadFile = File(...), db=Depends(get_db)):
    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="File must be JSON format")
    if db[COLLECTION_NAME] is None:
        raise HTTPException(status_code=401, detail="Collection not found") 

    raw = await file.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    docs = data if isinstance(data, list) else [data]
    if not docs:
        raise HTTPException(status_code=400, detail="Empty JSON file")

    missing_id = [i for i, d in enumerate(docs) if not isinstance(d, dict) or "id" not in d]
    if missing_id:
        raise HTTPException(status_code=400, detail=f"Missing 'id' at indexes: {missing_id}")

    uploaded_ids = [d["id"] for d in docs]

    seen = set()
    dup = sorted({x for x in uploaded_ids if x in seen or seen.add(x)})
    if dup:
        raise HTTPException(status_code=400, detail=f"Duplicate IDs in file: {dup}")

    existing_docs = await db[COLLECTION_NAME].find(
        {"id": {"$in": uploaded_ids}},
        {"_id": 0, "id": 1}
    ).to_list(length=None)

    existing_ids = [d["id"] for d in existing_docs]
    if existing_ids:
        raise HTTPException(status_code=409, detail=f"IDs already exist: {existing_ids}")

    
    try:
        insert_result = await db[COLLECTION_NAME].insert_many(docs, ordered=False)
        inserted = len(insert_result.inserted_ids)
    except Exception:
        raise HTTPException(status_code=500, detail="Insert failed")

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "Upload successful",
            "inserted": inserted,
            "total": len(docs)
        },
    )
    
@router.delete("/re/delete-by-ids", status_code=status.HTTP_200_OK)
async def delete_by_ids_endpoint(file: UploadFile = File(...), db=Depends(get_db)):
    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="File must be JSON format")

    raw = await file.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    ids = []

    if isinstance(data, list):
        if all(isinstance(x, (str, int)) for x in data):
            ids = data
        elif all(isinstance(x, dict) for x in data):
            if any("id" not in x for x in data):
                raise HTTPException(status_code=400, detail="Some objects missing 'id' field")
            ids = [x["id"] for x in data]
        else:
            raise HTTPException(status_code=400, detail="Invalid array format")
    elif isinstance(data, dict) and "ids" in data:
        if not isinstance(data["ids"], list):
            raise HTTPException(status_code=400, detail="'ids' field must be an array")
        ids = data["ids"]
    else:
        raise HTTPException(status_code=400, detail="JSON must be array or object with 'ids'")

    ids = [x for x in ids if x is not None]
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    seen = set()
    unique_ids = []
    for x in ids:
        if x not in seen:
            seen.add(x)
            unique_ids.append(x)

    try:
        existing = await db.COLLECTION_NAME.find(
            {"id": {"$in": unique_ids}},
            {"_id": 0, "id": 1}
        ).to_list(length=None)
        existing_ids = {d["id"] for d in existing}

        not_found = [x for x in unique_ids if x not in existing_ids]

        del_result = await db[COLLECTION_NAME].delete_many({"id": {"$in": unique_ids}})
        print(db[COLLECTION_NAME].find({})[0])
        deleted_count = int(del_result.deleted_count)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Delete operation completed",
                "deleted": deleted_count,
                "not_found": not_found,
                "total_ids": len(unique_ids)
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Delete error: {e}")
        raise HTTPException(status_code=500, detail="Delete operation failed")
    
# @router.delete("/re/delete-all", status_code=status.HTTP_200_OK)
# # async def delete_all():
# #     try

# #     except:
# #     return
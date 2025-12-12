import json
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.api.deps import get_db
from app.services.label_studio import (
    get_all_labeled_data,
    process_and_store_labeled_data,
    delete_all_labeled_data,
)

router = APIRouter(
    tags=["NER labeled Data"]
)

COLLECTION_NAME = os.getenv("NER_LABELED_COLLECTION", "ner_labeled")

@router.post("/ner/insert-many", status_code=status.HTTP_201_CREATED)
async def upload_json(file: UploadFile, db=Depends(get_db)):
    
    if file.content_type not in ("application/json", "text/json"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        raw = await file.read()
        data = json.loads(raw)
        docs = data if isinstance(data, list) else [data]
        if not docs:
            raise HTTPException(status_code=400, detail="Empty JSON")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="File processing failed")

    try:
        collection = db[COLLECTION_NAME]
        result = await process_and_store_labeled_data(collection, docs)
        return {"inserted": result["inserted"]}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Store failed")


@router.delete("/ner/delete-all", status_code=status.HTTP_200_OK)
async def delete_all_docs(db=Depends(get_db)):
    try:
        collection = db[COLLECTION_NAME]
        result = await delete_all_labeled_data(collection)
        return {"deleted": result["deleted"]}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Delete failed")


@router.get("/ner/get-all", status_code=status.HTTP_200_OK)
async def get_all_docs(db=Depends(get_db)):
    try:
        collection = db[COLLECTION_NAME]
        docs = get_all_labeled_data(collection)
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
        return {"total": len(docs), "data": docs}
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Fetch failed")

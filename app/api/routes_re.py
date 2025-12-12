from typing import List, Optional, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.re_infer import predict_relations

router = APIRouter(prefix="", tags=["relation-extraction"])

class EntitySpan(BaseModel):
    text: str
    type: str
    start: Optional[int] = None
    end: Optional[int] = None

class PairInput(BaseModel):
    e1: EntitySpan
    e2: EntitySpan

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1)
    pairs: List[PairInput] = Field(default_factory=list)

class PredictResponseItem(BaseModel):
    e1: EntitySpan
    e2: EntitySpan
    relation: str
    confidence: float

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/predict-re", response_model=List[PredictResponseItem])
def predict_re(req: PredictRequest):
    if not req.pairs:
        return []
    pairs = [p.model_dump() for p in req.pairs]
    return predict_relations(req.text, pairs)

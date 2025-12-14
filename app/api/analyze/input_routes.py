from typing import Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/text", tags=["Text Analysis"])

class TextIn(BaseModel):
    text: str = Field(..., min_length=1, description="Input text to analyze")

class BaseResponse(BaseModel):
    status: int
    message: str
    data: Any

@router.post(
    "/analyze",
    response_model=BaseResponse,
    status_code=status.HTTP_200_OK
)
def analyze(payload: TextIn):
    text = payload.text.strip()

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text is empty"
        )

    return BaseResponse(
        status=200,
        message="success",  
        data= text
    )

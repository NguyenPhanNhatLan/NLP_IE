import json
import logging
import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse


router = APIRouter(
    tags=["Data Receiver"]
)


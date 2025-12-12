from fastapi import FastAPI
from app.api.labeled import ner_labeled, re_labeled
from app.api.routes_re import router as re_routes

app = FastAPI()

app.include_router(ner_labeled.router, prefix="/api/labeled_data")
app.include_router(re_labeled.router, prefix="/api/labeled_data")
app.include_router(re_routes)


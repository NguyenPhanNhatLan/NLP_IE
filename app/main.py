from fastapi import FastAPI
from app.api.ner import ner_routes
from app.api.re import re_routes
from app.api.ner import ner_routes
from app.api.analyze import input_routes
app = FastAPI()


app.include_router(re_routes.router)
app.include_router(ner_routes.router)
app.include_router(input_routes.router)

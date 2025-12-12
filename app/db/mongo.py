from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings


def get_mongo_client() -> MongoClient:
    try:
        client = MongoClient(settings.mongo_uri)
        client.admin.command("ping")
        print("MongoDB connected")
        return client
    except ConnectionFailure as e:
        raise RuntimeError(f"MongoDB connection failed: {e}")


def get_database():
    client = get_mongo_client()
    return client[settings.mongo_db]

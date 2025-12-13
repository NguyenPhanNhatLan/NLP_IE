from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
from app.core.config import settings

_client: AsyncIOMotorClient | None = None


async def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client:
        return _client

    try:
        client = AsyncIOMotorClient(settings.mongo_uri)
        await client.admin.command("ping")
        print("MongoDB async connected")
        _client = client
        return client
    except ConnectionFailure as e:
        raise RuntimeError(f"MongoDB connection failed: {e}")


async def get_database() -> AsyncIOMotorDatabase:
    client = await get_mongo_client()
    return client[settings.mongo_db]

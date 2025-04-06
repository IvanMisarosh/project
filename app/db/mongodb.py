from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
if settings.MONGODB_NAME:
    db = client[settings.MONGODB_NAME]
else:
    db = client.get_database("comment_db")

if settings.MONGODB_COLLECTION:
    comments_collection = db[settings.MONGODB_COLLECTION]
else:
    comments_collection = db.get_collection("comments")

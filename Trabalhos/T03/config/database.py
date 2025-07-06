from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
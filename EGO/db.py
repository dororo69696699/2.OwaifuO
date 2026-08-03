from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# MongoDB Connection
client = AsyncIOMotorClient(MONGO_URL)
db = client["WAIFUBOT"]

# Existing Collections
Users = db["USERS"]
Groups = db["GROUPS"]
Banned = ["BANNED"]
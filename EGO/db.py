from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

# MongoDB Connection
client = AsyncIOMotorClient(MONGO_URL)
db = client["waifucluster"]

# USERS AND GROUPS

Users = db["USERS"]
Groups = db["GROUPS"]
Banned = ["BANNED"]

# CHARACTER 

collection = db['anime_characters_lol']
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
discounts_collection = db['discounts']
redeem_collection = db["redeem_codes"]

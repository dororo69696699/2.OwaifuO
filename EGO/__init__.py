from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import logging

# 🔥 Logging Setup
logging.basicConfig(
    format="[Naruto-Bot] %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("/app/logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

# 🔥 Main Bot Client
bot = Client(
    "Waifu-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="EGO/Modules")
)

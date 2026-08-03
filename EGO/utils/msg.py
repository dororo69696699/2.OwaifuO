# EGO/modules/msg.py

from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from EGO import bot
from EGO.db import Groups

@bot.on_message(filters.group & ~filters.bot & ~filters.service)
async def count_messages(client: Client, message: Message):
    chat_id = message.chat.id

    # Update message count in database
    await Groups.update_one(
        {"id": chat_id},
        {
            "$inc": {"message_count": 1},  # Increment by 1
            "$set": {
                "title": message.chat.title,
                "username": message.chat.username,
                "last_activity": datetime.now()
            }
        },
        upsert=True
    )

# Get count from database
async def get_message_count(chat_id):
    group = await Groups.find_one({"id": chat_id})
    return group.get("message_count", 0) if group else 0

# Reset count in database
async def reset_message_count(chat_id):
    await Groups.update_one(
        {"id": chat_id},
        {"$set": {"message_count": 0}}
    )

# Check spawn condition
async def should_spawn(chat_id, threshold=100):
    count = await get_message_count(chat_id)
    return count >= threshold
import os
import random
import time
from pyrogram import Client, enums, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from EGO import bot
from EGO.db import Users, Groups
from config import START_IMG

START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# Private Start Message Generator
async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name
    
    msg_date = getattr(message, "date", None)
    ping = round(time.time() - msg_date.timestamp(), 2) if msg_date else 0.0
    uptime = get_uptime()

    caption = (
        f"🌸 <b>ᴏʜ ᴍʏ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɴᴇᴢᴜᴋᴏ's ᴡᴏʀʟᴅ!</b> 🎀\n\n"
        f"<i>ʜᴍᴍᴘʜ~ ɪ ᴀᴍ {bot_name}! ɪ ᴘʀᴏᴛᴇᴄᴛ ᴍʏ ᴏɴɪɪ-ᴄʜᴀɴ ᴀɴᴅ ᴀʟʟ ᴍʏ ғʀɪᴇɴᴅs! "
        f"ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ, ɪ ᴡᴏɴ'ᴛ ʙɪᴛᴇ... ᴜɴʟᴇss ʏᴏᴜ'ʀᴇ ᴀ ʙᴀᴅ ᴅᴇᴍᴏɴ!</i> 💖\n\n"
        f"<blockquote>━━━━━━━▧▣▧━━━━━━━\n"
        f"⦾ <b>ᴍʏ ᴍɪssɪᴏɴ:</b> ɪ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘs ᴀɴᴅ ʜᴇʟᴘ ᴍᴀɴᴀɢᴇ ᴇᴠᴇʀʏᴛʜɪɴɢ!\n"
        f"⦾ <b>ʜᴏᴡ ᴛᴏ ᴜsᴇ:</b> ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ sᴇᴇ ᴍʏ ᴘᴏᴡᴇʀs!\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"⚡ <b>sᴘᴇᴇᴅ:</b> <code>{ping}</code> ᴍs\n"
        f"⏳ <b>ᴀᴄᴛɪᴠᴇ ᴛɪᴍᴇ:</b> <code>{uptime}</code></blockquote>"
    )

    buttons = [
        [InlineKeyboardButton("🎀 ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [
            InlineKeyboardButton("💗 sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ],
        [InlineKeyboardButton("👤 ᴏᴡɴᴇʀ", url="https://t.me/EGOIST_6969")]
    ]

    return caption, buttons

# Group Start Message Generator
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = (
        f"🎀 <i>ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ ɪ ᴀᴍ</i> <b>{bot_user.first_name}</b> 🌸\n\n"
        f"<blockquote>ɪ'ᴍ ʜᴇʀᴇ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴛʜɪs ᴄʜᴀᴛ ᴀɴᴅ ʜᴇʟᴘ ᴇᴠᴇʀʏᴏɴᴇ! "
        f"ɪ ᴡɪʟʟ ᴋɪᴄᴋ ᴀᴡᴀʏ ᴀʟʟ ᴛʜᴇ ʙᴀᴅ ᴘᴇᴏᴘʟᴇ ᴀɴᴅ ᴋᴇᴇᴘ ᴇᴠᴇʀʏᴏɴᴇ sᴀғᴇ!\n\n"
        f"ʟᴇᴛ's ʜᴀᴠᴇ ғᴜɴ ᴛᴏɢᴇᴛʜᴇʀ! 💖</blockquote>"
    )
    buttons = [
        [
            InlineKeyboardButton("💗 sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("📢 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ]
    ]
    return caption, buttons

# Send Photo Helper
async def send_photo_message(message, photo, caption, buttons):
    await message.reply_photo(
        photo=photo, 
        caption=caption, 
        reply_markup=InlineKeyboardMarkup(buttons), 
        parse_mode=enums.ParseMode.HTML
    )

# Private Start Command Handler
@bot.on_message(filters.command("start") & filters.private)
async def start_private_command(client, message):
    existing_user = await Users.find_one({"id": message.from_user.id})

    if not existing_user:
        user_data = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "start_time": time.time()
        }
        await Users.insert_one(user_data)

    caption, buttons = await generate_start_message(client, message)
    
    # Random image from START_IMG list
    start_image = random.choice(START_IMG) if isinstance(START_IMG, list) else START_IMG

    await send_photo_message(message, start_image, caption, buttons)

# Group Start Command Handler
@bot.on_message(filters.command("start") & filters.group)
async def start_group_command(client, message):
    # Save group info
    existing_group = await Groups.find_one({"id": message.chat.id})
    
    if not existing_group:
        group_data = {
            "id": message.chat.id,
            "title": message.chat.title,
            "username": message.chat.username,
            "added_time": time.time()
        }
        await Groups.insert_one(group_data)
    
    caption, buttons = await generate_group_start_message(client)
    start_image = random.choice(START_IMG) if isinstance(START_IMG, list) else START_IMG
    await send_photo_message(message, start_image, caption, buttons)
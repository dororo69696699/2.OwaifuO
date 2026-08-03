# EGO/modules/grab.py

from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from EGO import bot
from EGO.db import collection, user_collection, group_user_totals_collection
from config import SPAWN_TIMEOUT

# Import active_spawns from spawn module
from EGO.Plugins.spawn import active_spawns

# ======================================================
# GRAB COMMAND
# ======================================================
@bot.on_message(filters.group & filters.command("grab"))
async def grab_character(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if spawn is active
    if chat_id not in active_spawns:
        return await message.reply_text(
            "🎀 <i>ɴᴏ ᴀᴄᴛɪᴠᴇ sᴘᴀᴡɴ ʀɪɢʜᴛ ɴᴏᴡ!</i>\n\n"
            "<blockquote>ᴡᴀɪᴛ ғᴏʀ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴛᴏ sᴘᴀᴡɴ ғɪʀsᴛ~</blockquote>",
            parse_mode=enums.ParseMode.HTML
        )
    
    spawn_data = active_spawns[chat_id]
    
    # Check if already grabbed
    if spawn_data["grabbed"]:
        return await message.reply_text(
            "🎀 <b>ᴛᴏᴏ ʟᴀᴛᴇ!</b>\n\n"
            "<blockquote>ʜᴍᴍᴘʜ~ ᴛʜɪs ᴄʜᴀʀᴀᴄᴛᴇʀ ᴡᴀs ᴀʟʀᴇᴀᴅʏ\n"
            "ɢʀᴀʙʙᴇᴅ ʙʏ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ! 💔</blockquote>",
            parse_mode=enums.ParseMode.HTML
        )
    
    # Check timeout
    spawn_time = spawn_data["spawn_time"]
    time_elapsed = datetime.now() - spawn_time
    
    if time_elapsed > timedelta(seconds=SPAWN_TIMEOUT):
        return await message.reply_text(
            "🎀 <b>ᴛɪᴍᴇ's ᴜᴘ!</b>\n\n"
            "<blockquote>ʜᴍᴍᴘʜ~ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ʀᴀɴ ᴀᴡᴀʏ ᴀʟʀᴇᴀᴅʏ!\n"
            "ʏᴏᴜ ᴡᴇʀᴇ ᴛᴏᴏ sʟᴏᴡ~ ⏰</blockquote>",
            parse_mode=enums.ParseMode.HTML
        )
    
    # Get guessed name
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text(
            "🎀 <b>ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ!</b>\n\n"
            "<blockquote>ᴘʟᴇᴀsᴇ ᴜsᴇ:\n"
            "<code>/grab character name</code></blockquote>\n\n"
            "<b>ᴇxᴀᴍᴘʟᴇ:</b>\n"
            "<code>/grab Nezuko Kamado</code>",
            parse_mode=enums.ParseMode.HTML
        )
    
    guessed_name = args[1].strip().lower()
    character = spawn_data["character"]
    actual_name = character.get("name", "").lower()
    
    # Check if name matches (flexible matching)
    if guessed_name not in actual_name and actual_name not in guessed_name:
        return await message.reply_text(
            f"🎀 <b>ᴡʀᴏɴɢ ɴᴀᴍᴇ!</b>\n\n"
            f"<blockquote>ʜᴍᴍᴘʜ~ <code>{args[1]}</code> ɪs ɴᴏᴛ ᴄᴏʀʀᴇᴄᴛ!\n"
            f"ᴛʀʏ ᴀɢᴀɪɴ! 💭</blockquote>",
            parse_mode=enums.ParseMode.HTML
        )
    
    # SUCCESS! Add to user collection
    spawn_data["grabbed"] = True
    
    # Calculate grab speed
    grab_time = (datetime.now() - spawn_time).total_seconds()
    
    # Update user collection
    user_data = {
        "user_id": user_id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "character_id": character.get("id"),
        "name": character.get("name"),
        "anime": character.get("anime"),
        "rarity": character.get("rarity"),
        "rarity_number": character.get("rarity_number"),
        "img_url": character.get("img_url"),
        "grabbed_at": datetime.now(),
        "grab_speed": grab_time,
        "chat_id": chat_id,
        "chat_title": message.chat.title
    }
    
    await user_collection.insert_one(user_data)
    
    # Update group stats
    await group_user_totals_collection.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {
            "$inc": {"count": 1},
            "$set": {
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "chat_title": message.chat.title
            }
        },
        upsert=True
    )
    
    # Get user's total count in this group
    user_stats = await group_user_totals_collection.find_one(
        {"user_id": user_id, "chat_id": chat_id}
    )
    total_grabbed = user_stats.get("count", 1) if user_stats else 1
    
    # Success message with details
    success_text = (
        f"🎀 <b>ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs!</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 {message.from_user.mention} sᴜᴄᴄᴇssғᴜʟʟʏ ɢʀᴀʙʙᴇᴅ:\n\n"
        f"🍁 <b>ɴᴀᴍᴇ:</b> {character.get('name')}\n"
        f"⛩️ <b>ᴀɴɪᴍᴇ:</b> {character.get('anime')}\n"
        f"🥀 <b>ʀᴀʀɪᴛʏ:</b> {character.get('rarity')}\n"
        f"🆔 <b>ɪᴅ:</b> <code>{character.get('id')}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚡ <b>ɢʀᴀʙ sᴘᴇᴇᴅ:</b> {grab_time:.2f}s\n"
        f"🎯 <b>ᴛᴏᴛᴀʟ ɢʀᴀʙs:</b> {total_grabbed}\n\n"
        f"<blockquote>ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ ɢʀᴇᴀᴛ ᴄᴀᴛᴄʜ!\n"
        f"ᴛʜᴇʏ'ʟʟ ʙᴇ sᴀғᴇ ɪɴ ʏᴏᴜʀ ʜᴀʀᴇᴍ! 💗</blockquote>"
    )
    
    # Send success with character image
    img_url = character.get("img_url")
    if img_url:
        await message.reply_photo(
            photo=img_url,
            caption=success_text,
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await message.reply_text(
            success_text,
            parse_mode=enums.ParseMode.HTML
        )
    
    # Remove from active spawns
    del active_spawns[chat_id]
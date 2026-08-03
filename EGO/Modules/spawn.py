# EGO/Modules/spawn.py

import random
import asyncio
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from EGO import bot
from EGO.db import collection, Groups
from EGO.utils.rarity import rarity_map
from config import SPAWN_TIMEOUT, DEFAULT_SPAWN_LIMIT

# Store active spawns and settings
active_spawns = {}
spawn_settings = {}

# ======================================================
# MESSAGE COUNTER + AUTO SPAWN SYSTEM
# ======================================================
@bot.on_message(filters.group & ~filters.bot & ~filters.service & ~filters.command(["grab", "ctime", "start", "upload", "rarity"]))
async def auto_spawn_checker(client: Client, message: Message):
    chat_id = message.chat.id
    
    # Update message count in database
    await Groups.update_one(
        {"id": chat_id},
        {
            "$inc": {"message_count": 1},
            "$set": {
                "title": message.chat.title,
                "username": message.chat.username,
                "last_activity": datetime.now()
            }
        },
        upsert=True
    )
    
    # Get current count
    group = await Groups.find_one({"id": chat_id})
    current_count = group.get("message_count", 0) if group else 0
    
    # Get spawn limit for this group
    spawn_limit = spawn_settings.get(chat_id, DEFAULT_SPAWN_LIMIT)
    
    # Check if should spawn
    if current_count >= spawn_limit:
        # Check if spawn already active
        if chat_id in active_spawns:
            return
        
        # Trigger spawn
        await trigger_spawn(client, message)
        
        # Reset message counter
        await Groups.update_one(
            {"id": chat_id},
            {"$set": {"message_count": 0}}
        )

# ======================================================
# TRIGGER SPAWN FUNCTION
# ======================================================
async def trigger_spawn(client: Client, message: Message):
    chat_id = message.chat.id
    
    try:
        # Get random character from database
        pipeline = [{"$sample": {"size": 1}}]
        cursor = collection.aggregate(pipeline)
        characters = await cursor.to_list(length=1)
        
        if not characters:
            return
        
        character = characters[0]
        
        # Determine if waifu or husbando
        gender = random.choice(["ᴡᴀɪғᴜ", "ʜᴜsʙᴀɴᴅᴏ"])
        
        # Get character details
        name = character.get("name", "ᴜɴᴋɴᴏᴡɴ")
        rarity = character.get("rarity", "⚪️ Common")
        char_id = character.get("id", "00")
        img_url = character.get("img_url")
        
        # Spawn caption
        caption = (
            f"🎀 ᴀ {rarity} {gender} ʜᴀs ᴀᴘᴘᴇᴀʀᴇᴅ!\n\n"
            f"<blockquote>ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ ᴀᴅᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ʜᴀʀᴇᴍ ʙʏ sᴇɴᴅɪɴɢ:\n\n"
            f"<code>/grab character name</code></blockquote>\n\n"
            f"⏰ ʏᴏᴜ ʜᴀᴠᴇ <b>{SPAWN_TIMEOUT // 60} ᴍɪɴᴜᴛᴇs</b> ᴛᴏ ɢʀᴀʙ!"
        )
        
        # Send spawn message
        if img_url:
            spawn_msg = await message.reply_photo(
                photo=img_url,
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            spawn_msg = await message.reply_text(
                text=caption,
                parse_mode=enums.ParseMode.HTML
            )
        
        # Store spawn data
        active_spawns[chat_id] = {
            "character": character,
            "spawn_time": datetime.now(),
            "message_id": spawn_msg.id,
            "grabbed": False
        }
        
        # Schedule timeout
        asyncio.create_task(spawn_timeout(client, chat_id, spawn_msg, char_id))
        
    except Exception as e:
        print(f"Spawn error: {e}")

# ======================================================
# SPAWN TIMEOUT HANDLER
# ======================================================
async def spawn_timeout(client: Client, chat_id: int, spawn_msg: Message, char_id: str):
    await asyncio.sleep(SPAWN_TIMEOUT)
    
    # Check if still active and not grabbed
    if chat_id in active_spawns and not active_spawns[chat_id]["grabbed"]:
        
        timeout_text = (
            f"🎀 <b>ᴛɪᴍᴇ's ᴜᴘ!</b>\n\n"
            f"<blockquote>ʜᴍᴍᴘʜ~ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ʀᴀɴ ᴀᴡᴀʏ\n"
            f"ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ɢʀᴀʙʙᴇᴅ ᴛʜᴇᴍ ɪɴ ᴛɪᴍᴇ! 💔</blockquote>\n\n"
            f"<i>ʙᴇ ғᴀsᴛᴇʀ ɴᴇxᴛ ᴛɪᴍᴇ!</i>"
        )
        
        # MORE INFO button
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("💗 ᴍᴏʀᴇ ɪɴғᴏ", callback_data=f"timeout_info_{char_id}_{chat_id}")]
        ])
        
        try:
            await spawn_msg.edit_caption(
                caption=timeout_text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        except:
            try:
                await spawn_msg.edit_text(
                    text=timeout_text,
                    reply_markup=buttons,
                    parse_mode=enums.ParseMode.HTML
                )
            except:
                pass
        
        # Remove from active spawns
        del active_spawns[chat_id]

# ======================================================
# MORE INFO CALLBACK (After Timeout)
# ======================================================
@bot.on_callback_query(filters.regex(r"^timeout_info_"))
async def timeout_info_callback(client: Client, query: CallbackQuery):
    try:
        data = query.data.split("_")
        char_id = data[2]
        
        # Get character from database
        character = await collection.find_one({"id": char_id})
        
        if not character:
            return await query.answer("🎀 ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ!", show_alert=True)
        
        # Character details
        name = character.get("name", "ᴜɴᴋɴᴏᴡɴ")
        anime = character.get("anime", "ᴜɴᴋɴᴏᴡɴ")
        rarity = character.get("rarity", "⚪️ Common")
        char_id = character.get("id", "00")
        img_url = character.get("img_url")
        
        info_text = (
            f"🎀 <b>ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴғᴏ</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🍁 <b>ɴᴀᴍᴇ:</b> {name}\n"
            f"⛩️ <b>ᴀɴɪᴍᴇ:</b> {anime}\n"
            f"🥀 <b>ʀᴀʀɪᴛʏ:</b> {rarity}\n"
            f"🆔 <b>ɪᴅ:</b> <code>{char_id}</code>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>ᴄʟɪᴄᴋᴇᴅ ʙʏ:</b> {query.from_user.mention}\n\n"
            f"<i>ʜᴍᴍᴘʜ~ ʏᴏᴜ ᴡᴇʀᴇ ᴛᴏᴏ ʟᴀᴛᴇ!</i>"
        )
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 ᴄʟᴏsᴇ", callback_data="close_info")]
        ])
        
        # Send info as new message with image
        if img_url:
            await query.message.reply_photo(
                photo=img_url,
                caption=info_text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.message.reply_text(
                text=info_text,
                reply_markup=buttons,
                parse_mode=enums.ParseMode.HTML
            )
        
        await query.answer()
        
    except Exception as e:
        await query.answer(f"🎀 ᴇʀʀᴏʀ: {str(e)}", show_alert=True)

# ======================================================
# CLOSE INFO CALLBACK
# ======================================================
@bot.on_callback_query(filters.regex("^close_info$"))
async def close_info(client: Client, query: CallbackQuery):
    await query.message.delete()
    await query.answer("🎀 ᴄʟᴏsᴇᴅ!", show_alert=False)
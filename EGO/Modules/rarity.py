# EGO/Modules/rarity.py

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from EGO import bot
from EGO.db import collection
from EGO.utils.rarity import rarity_map

# ======================================================
# RARITY LIST COMMAND
# ======================================================
@bot.on_message(filters.command("rarity"))
async def rarity_list(client: Client, message: Message):
    try:
        text = "🎀 <b>ɴᴇᴢᴜᴋᴏ's ʀᴀʀɪᴛʏ ʟɪsᴛ</b>\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        total = 0
        
        # Loop through all rarities
        for rarity_no in sorted(rarity_map.keys()):
            rarity_name = rarity_map[rarity_no]
            
            # Count characters with this rarity
            count = await collection.count_documents(
                {"rarity_number": rarity_no}
            )
            
            total += count
            
            # Get emoji from rarity name
            emoji = rarity_name.split()[0] if rarity_name else "🎀"
            
            text += (
                f"{emoji} <b>{rarity_name}</b>\n"
                f"   ↬ <code>{count}</code> ᴄʜᴀʀᴀᴄᴛᴇʀs\n\n"
            )
        
        text += "━━━━━━━━━━━━━━━━━━━━━\n"
        text += f"🎯 <b>ᴛᴏᴛᴀʟ:</b> <code>{total}</code> ᴄʜᴀʀᴀᴄᴛᴇʀs\n\n"
        text += "<blockquote><i>ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ sᴏ ᴍᴀɴʏ\n"
        text += "ғʀɪᴇɴᴅs ᴛᴏ ᴄᴏʟʟᴇᴄᴛ!</i></blockquote>\n\n"
        text += "💗 <b>ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ</b>"
        
        await message.reply_text(
            text,
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        await message.reply_text(
            f"🎀 <i>ᴇʀʀᴏʀ:</i> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML
        )


# ======================================================
# TOTAL CHARACTERS COMMAND
# ======================================================
@bot.on_message(filters.command("total"))
async def total_characters(client: Client, message: Message):
    try:
        # Count total characters in database
        total = await collection.count_documents({})
        
        # Count by category
        common_count = await collection.count_documents({"rarity_number": 1})
        legendary_count = await collection.count_documents({"rarity_number": 2})
        special_count = await collection.count_documents({"rarity_number": 3})
        limited_count = await collection.count_documents({"rarity_number": 4})
        
        # Calculate rare characters (rarity > 4)
        rare_count = total - (common_count + legendary_count + special_count + limited_count)
        
        text = (
            f"🎀 <b>ᴅᴀᴛᴀʙᴀsᴇ sᴛᴀᴛs</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📊 <b>ᴛᴏᴛᴀʟ ᴄʜᴀʀᴀᴄᴛᴇʀs:</b> <code>{total}</code>\n\n"
            f"<blockquote>"
            f"⚪️ ᴄᴏᴍᴍᴏɴ: <code>{common_count}</code>\n"
            f"🟡 ʟᴇɢᴇɴᴅᴀʀʏ: <code>{legendary_count}</code>\n"
            f"💮 sᴘᴇᴄɪᴀʟ: <code>{special_count}</code>\n"
            f"🔮 ʟɪᴍɪᴛᴇᴅ: <code>{limited_count}</code>\n"
            f"✨ ʀᴀʀᴇ & ᴏᴛʜᴇʀs: <code>{rare_count}</code>"
            f"</blockquote>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>ʜᴍᴍᴘʜ~ ᴜsᴇ /rarity ᴛᴏ sᴇᴇ\n"
            f"ᴄᴏᴍᴘʟᴇᴛᴇ ʀᴀʀɪᴛʏ ʙʀᴇᴀᴋᴅᴏᴡɴ!</i>\n\n"
            f"💗 <b>ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ</b>"
        )
        
        await message.reply_text(
            text,
            parse_mode=enums.ParseMode.HTML
        )
        
    except Exception as e:
        await message.reply_text(
            f"🎀 <i>ᴇʀʀᴏʀ:</i> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML
        )
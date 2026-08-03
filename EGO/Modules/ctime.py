# EGO/Modules/ctime.py

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from EGO import bot
from config import OWNER_ID

# Import spawn_settings from spawn.py
from EGO.Modules.spawn import spawn_settings

# ======================================================
# SET SPAWN TIME COMMAND (Admin Only)
# ======================================================
@bot.on_message(filters.group & filters.command("ctime"))
async def set_spawn_time(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Direct owner check
    is_owner = (user_id == OWNER_ID)
    
    # Admin check
    is_admin = False
    try:
        member = await message.chat.get_member(user_id)
        is_admin = member.status in ["creator", "administrator"]
    except Exception:
        pass
    
    # Allow if owner OR admin
    if not (is_owner or is_admin):
        return await message.reply_text(
            "🎀 <i>ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!</i>",
            parse_mode=enums.ParseMode.HTML
        )
    
    args = message.text.split()
    if len(args) != 2:
        return await message.reply_text(
            "🎀 <b>ᴜsᴀɢᴇ:</b>\n\n"
            "<code>/ctime message_count</code>\n\n"
            "<b>ᴇxᴀᴍᴘʟᴇ:</b>\n"
            "<code>/ctime 100</code>\n\n"
            "<blockquote>sᴘᴀᴡɴ ᴡɪʟʟ ᴛʀɪɢɢᴇʀ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ 100 ᴍᴇssᴀɢᴇs\n\n"
            "ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ sᴘᴀᴡɴ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 80 ᴛᴏ 500 ᴍᴇssᴀɢᴇs</blockquote>",
            parse_mode=enums.ParseMode.HTML
        )
    
    try:
        count = int(args[1])
        
        # Bot owner can set any value (1-1000)
        if is_owner:
            if count < 1 or count > 1000:
                return await message.reply_text(
                    "🎀 <i>ᴘʟᴇᴀsᴇ sᴇᴛ ᴀ ᴠᴀʟᴜᴇ ʙᴇᴛᴡᴇᴇɴ 1-1000!</i>",
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            # Group admins must follow 80-500 range
            if count < 80 or count > 500:
                return await message.reply_text(
                    "🎀 <i>ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ sᴘᴀᴡɴ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 80 ᴛᴏ 500 ᴍᴇssᴀɢᴇs!</i>",
                    parse_mode=enums.ParseMode.HTML
                )
        
        # Save spawn settings
        spawn_settings[chat_id] = count
        
        await message.reply_text(
            f"✅ <b>sᴘᴀᴡɴ ᴛɪᴍᴇ sᴇᴛ!</b>\n\n"
            f"<blockquote>ɴᴇᴡ sᴘᴀᴡɴ ᴡɪʟʟ ᴛʀɪɢɢᴇʀ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ\n"
            f"<b>{count}</b> ᴍᴇssᴀɢᴇs!</blockquote>\n\n"
            f"🎀 <i>ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ ɢᴏᴏᴅ ʟᴜᴄᴋ!</i>",
            parse_mode=enums.ParseMode.HTML
        )
        
    except ValueError:
        await message.reply_text(
            "🎀 <i>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!</i>",
            parse_mode=enums.ParseMode.HTML
        )
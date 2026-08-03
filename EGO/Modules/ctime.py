import random
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from EGO import bot
from EGO.Modules.msg import get_message_count, reset_message_count, should_spawn
from config import SPAWN_TIMEOUT, DEFAULT_SPAWN_LIMIT, OWNER_ID

# ======================================================
# SET SPAWN TIME COMMAND (Admin Only)
# ======================================================
@bot.on_message(filters.group & filters.command("ctime"))
async def set_spawn_time(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if user is admin or owner
    member = await message.chat.get_member(user_id)
    is_admin = member.status in ["creator", "administrator"]
    is_owner = user_id == OWNER_ID

    if not is_admin and not is_owner:
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

        # Check limits based on user role
        if is_owner:
            # Owner can set any value (no minimum restriction)
            if count < 1 or count > 1000:
                return await message.reply_text(
                    "🎀 <i>ᴘʟᴇᴀsᴇ sᴇᴛ ᴀ ᴠᴀʟᴜᴇ ʙᴇᴛᴡᴇᴇɴ 1-1000!</i>",
                    parse_mode=enums.ParseMode.HTML
                )
        else:
            # Admins must follow 80-500 range
            if count < 80 or count > 500:
                return await message.reply_text(
                    "🎀 <i>ᴀᴅᴍɪɴs ᴄᴀɴ sᴇᴛ sᴘᴀᴡɴ ᴛɪᴍᴇ ʙᴇᴛᴡᴇᴇɴ 80 ᴛᴏ 500 ᴍᴇssᴀɢᴇs!</i>",
                    parse_mode=enums.ParseMode.HTML
                )

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
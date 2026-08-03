import os
import requests
import asyncio
import base64
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from EGO import bot
from EGO.db import collection, Groups
from EGO.utils.rarity import rarity_map
from config import IMGBB_API_KEY, CHARA_CHANNEL_ID, OWNER_ID

WRONG_FORMAT_TEXT = """🎀 <b>ᴏᴏᴘs! ᴡʀᴏɴɢ ғᴏʀᴍᴀᴛ~</b>

━━━━━━━━━━━━━━━━━━━━━

<blockquote>ᴘʟᴇᴀsᴇ ᴜsᴇ ᴛʜᴇ ᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ:</blockquote>

<code>/upload character-name anime-name rarity_number</code>

<blockquote>ᴇxᴀᴍᴘʟᴇ:</blockquote>
<code>/upload nezuko-kamado demon-slayer 1</code>

<blockquote>ᴀᴠᴀɪʟᴀʙʟᴇ ʀᴀʀɪᴛɪᴇs:</blockquote>
🔹 1 - ⚪️ ᴄᴏᴍᴍᴏɴ
🔹 2 - 🟡 ʟᴇɢᴇɴᴅᴀʀʏ
🔹 3 - 💮 sᴘᴇᴄɪᴀʟ
🔹 4 - 🔮 ʟɪᴍɪᴛᴇᴅ
🔹 5 - 💸 ᴘʀᴇᴍɪᴜᴍ
🔹 6 - 🌤 sᴜᴍᴍᴇʀ
🔹 7 - 🎐 ᴄᴇʟᴇsᴛɪᴀʟ
🔹 8 - ❄️ ᴡɪɴᴛᴇʀ
🔹 9 - 💝 ᴠᴀʟᴇɴᴛɪɴᴇ
🔹 10 - 🎃 ʜᴀʟʟᴏᴡᴇᴇɴ
🔹 11 - 🎄 ᴄʜʀɪsᴛᴍᴀs sᴘᴇᴄɪᴀʟ
🔹 12 - 🧧 ᴇᴠᴇɴᴛs
🔹 13 - 🍑 ᴇᴄʜʜɪ
🔹 14 - 🎗️ ᴀᴍᴠ
🔹 15 - 🌧 ʀᴀɪɴʏ
🔹 16 - 🦠 ᴍʏᴛʜɢᴀʀᴅ

━━━━━━━━━━━━━━━━━━━━━
💗 <b>ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ</b>"""

# ======================================================
# FIND NEXT ID
# ======================================================
async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []
    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except:
                continue

    ids.sort()
    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)

    return str(len(ids) + 1).zfill(2)


# ======================================================
# SMART UPLOAD - Handles both Catbox and ImgBB
# ======================================================
def smart_upload(file_path, media_type):
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Try ImgBB first for images
        if media_type == "image":
            try:
                with open(file_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")

                r = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": IMGBB_API_KEY, "image": encoded},
                    timeout=60
                )

                data = r.json()
                if data.get("success"):
                    return data["data"]["url"]
            except Exception as e:
                print(f"ImgBB upload failed, falling back to Catbox: {e}")

        # Fallback to Catbox
        files = {"fileToUpload": open(file_path, "rb")}
        data = {"reqtype": "fileupload"}

        r = requests.post("https://catbox.moe/user/api.php", files=files, data=data, timeout=120)

        if r.status_code == 200:
            url = r.text.strip()
            if url.startswith("https://"):
                return url

        raise Exception(f"Catbox upload failed: {r.text}")

    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")


upload_lock = asyncio.Lock()


# ======================================================
# UPLOAD COMMAND
# ======================================================
@bot.on_message(filters.command(["upload"]) & filters.user(OWNER_ID))
async def ul(client: Client, message: Message):
    if upload_lock.locked():
        return await message.reply_text(
            "🎀 <i>ʜᴍᴍᴘʜ~ ᴀɴᴏᴛʜᴇʀ ᴜᴘʟᴏᴀᴅ ɪs ɪɴ ᴘʀᴏɢʀᴇss...</i>",
            parse_mode=enums.ParseMode.HTML
        )

    async with upload_lock:
        reply = message.reply_to_message
        if not reply:
            return await message.reply_text(
                "🎀 <i>ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ғɪʟᴇ/ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ ᴡɪᴛʜ /upload</i>",
                parse_mode=enums.ParseMode.HTML
            )

        args = message.text.strip().split()
        if len(args) != 4:
            return await client.send_message(
                message.chat.id, 
                WRONG_FORMAT_TEXT,
                parse_mode=enums.ParseMode.HTML
            )

        try:
            character_name = args[1].replace('-', ' ').title()
            anime = args[2].replace('-', ' ').title()
            rarity = int(args[3])
        except:
            return await message.reply_text(
                "🎀 <i>ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ɪɴᴘᴜᴛ.</i>",
                parse_mode=enums.ParseMode.HTML
            )

        if rarity not in rarity_map:
            return await message.reply_text(
                f"🎀 <i>ɪɴᴠᴀʟɪᴅ ʀᴀʀɪᴛʏ ᴠᴀʟᴜᴇ. ᴀᴠᴀɪʟᴀʙʟᴇ ʀᴀʀɪᴛɪᴇs: {', '.join(map(str, rarity_map.keys()))}</i>",
                parse_mode=enums.ParseMode.HTML
            )

        rarity_text = rarity_map[rarity]
        available_id = await find_available_id()

        character = {
            "name": character_name,
            "anime": anime,
            "rarity": rarity_text,
            "rarity_number": rarity,
            "id": available_id
        }

        processing_message = await message.reply_text(
            "🎀 <i>ʜᴍᴍᴘʜ~ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛʜᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ...</i>",
            parse_mode=enums.ParseMode.HTML
        )

        path = None
        thumb_path = None

        try:
            # Download media
            path = await reply.download()
            if not path:
                raise Exception("Failed to download media")

            # Handle different media types
            if reply.photo:
                url = smart_upload(path, "image")
                character["img_url"] = url

            elif reply.document:
                if "image" in reply.document.mime_type:
                    url = smart_upload(path, "image")
                    character["img_url"] = url
                else:
                    url = smart_upload(path, "video")
                    character["vid_url"] = url

            elif reply.video:
                url = smart_upload(path, "video")
                character["vid_url"] = url

                try:
                    thumbs = getattr(reply.video, "thumbs", None)
                    if thumbs:
                        thumb_path = await client.download_media(thumbs[0].file_id)
                        turl = smart_upload(thumb_path, "image")
                        character["thum_url"] = turl
                except Exception as e:
                    print(f"Thumbnail upload failed: {e}")

            else:
                raise Exception("Unsupported media type")

            caption_text = (
                f"🎀 <b>ɴᴇᴡ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴅᴅᴇᴅ</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📛 <b>ɴᴀᴍᴇ:</b> {character_name}\n"
                f"⛩️ <b>ᴀɴɪᴍᴇ:</b> {anime}\n"
                f"🌈 <b>ʀᴀʀɪᴛʏ:</b> {rarity_text}\n"
                f"🆔 <b>ɪᴅ:</b> {available_id}\n"
                f"👤 <b>ᴀᴅᴅᴇᴅ ʙʏ:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🌸\n"
                f"<i>\"ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ ᴀɴᴏᴛʜᴇʀ ᴏɴᴇ\n"
                f"ᴊᴏɪɴs ᴏᴜʀ ғᴀᴍɪʟʏ!\"</i>\n\n"
                f"💗 <b>ɴᴇᴢᴜᴋᴏ ᴋᴀᴍᴀᴅᴏ</b>"
            )

            # Send to channel
            if "img_url" in character:
                await client.send_photo(
                    CHARA_CHANNEL_ID, 
                    character["img_url"], 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )
            elif "vid_url" in character:
                await client.send_video(
                    CHARA_CHANNEL_ID, 
                    character["vid_url"], 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await client.send_document(
                    CHARA_CHANNEL_ID, 
                    path, 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )

            # Insert into database
            await collection.insert_one(character)

            await processing_message.edit_text(
                f"✅ <b>ᴄʜᴀʀᴀᴄᴛᴇʀ ᴜᴘʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n"
                f"📛 <b>ɴᴀᴍᴇ:</b> {character_name}\n"
                f"🆔 <b>ɪᴅ:</b> {available_id}\n"
                f"🌈 <b>ʀᴀʀɪᴛʏ:</b> {rarity_text}\n\n"
                f"🎀 ʜᴍᴍᴘʜ~ ᴀɴᴏᴛʜᴇʀ ғʀɪᴇɴᴅ ᴊᴏɪɴᴇᴅ!",
                parse_mode=enums.ParseMode.HTML
            )

        except Exception as e:
            await processing_message.edit_text(
                f"❌ <b>ᴜᴘʟᴏᴀᴅ ғᴀɪʟᴇᴅ</b>\n\n"
                f"<code>{str(e)}</code>\n\n"
                f"🎀 <i>ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ɪɴᴘᴜᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</i>",
                parse_mode=enums.ParseMode.HTML
            )

        finally:
            # Clean up temporary files
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
            if thumb_path and os.path.exists(thumb_path):
                try:
                    os.remove(thumb_path)
                except:
                    pass


# ======================================================
# RARITY COUNT COMMAND
# ======================================================
@bot.on_message(filters.command("rarity"))
async def rarity_count(client: Client, message: Message):
    try:
        text = "🎀 <b>ɴᴇᴢᴜᴋᴏ's ʀᴀʀɪᴛʏ ʟɪsᴛ</b>\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n\n"

        total = 0

        for rarity_no in sorted(rarity_map.keys()):
            rarity_name = rarity_map[rarity_no]

            count = await collection.count_documents(
                {"rarity_number": rarity_no}
            )

            total += count

            # Get emoji for rarity
            rarity_emoji = {
                '⚪️ Common': '⚪️',
                '🟡 Legendary': '🟡',
                '💮 Special': '💮',
                '🔮 Limited': '🔮',
                '💸 Premium': '💸',
                '🌤 Summer': '🌤',
                '🎐 Celestial': '🎐',
                '❄️ Winter': '❄️',
                '💝 Valentine': '💝',
                '🎃 Halloween': '🎃',
                '🎄 Christmas Special': '🎄',
                '🧧 Events': '🧧',
                '🍑 Echhi': '🍑',
                '🎗️ AMV': '🎗️',
                '🌧 Rainy': '🌧',
                '🦠 Mythgard': '🦠'
            }.get(rarity_name, '🎀')

            text += (
                f"{rarity_emoji} <b>{rarity_name}</b>\n"
                f"   ↬ {count} ᴄʜᴀʀᴀᴄᴛᴇʀs\n\n"
            )

        text += "━━━━━━━━━━━━━━━━━━━━━\n"
        text += f"🎀 <b>ᴛᴏᴛᴀʟ</b> ↬ {total} ᴄʜᴀʀᴀᴄᴛᴇʀs\n\n"
        text += "<i>\"ʜᴍᴍᴘʜ ʜᴍᴍᴘʜ~ sᴏ ᴍᴀɴʏ\n"
        text += "ғʀɪᴇɴᴅs ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ!\"</i>\n\n"
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
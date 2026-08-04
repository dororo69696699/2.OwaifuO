from pyrogram import enums
from pyrogram.types import Message
from config import OWNER_ID

async def is_admin(message: Message) -> bool:
    """
    Check if user is admin or owner
    Returns True if user is group admin/creator or bot owner
    """
    user_id = message.from_user.id

    # ✅ Bot owner can ALWAYS use (highest priority)
    if user_id == OWNER_ID:
        return True

    # Check if in group
    if not message.chat:
        return False

    try:
        # Check if user is admin in group
        member = await message.chat.get_member(user_id)

        # ✅ Use Pyrogram enums instead of raw strings
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
            return True
        else:
            return False

    except Exception as e:
        print(f"⚠️ Admin check error: {e}")
        # If error and user is owner, still allow
        if user_id == OWNER_ID:
            return True
        return False
import os

API_ID = int(os.getenv("API_ID", "31963776"))
API_HASH = os.getenv("API_HASH", "d352f599aff861566030a3cbba3a0f75")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8988622858:AAHamrsZ_mCiTB4L950B7k7Y8QApzcWPDRc")
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://Egoist:jayesh1090@waifubot.jblumsy.mongodb.net/?appName=Waifubot"
)

# Card System Configurations
DEFAULT_SPAWN_LIMIT = int(os.getenv("DEFAULT_SPAWN_LIMIT", "100"))

SPAWN_TIMEOUT = int(os.getenv("SPAWN_TIMEOUT", "300"))  # 5 minutes in seconds

TRADE_TIMEOUT = int(os.getenv("TRADE_TIMEOUT", "600"))  # 10 minutes

# START IMAGES
START_IMG = [
    "https://files.catbox.moe/nsbcfh.jpg",
    "https://files.catbox.moe/nd8gpf.jpg",
    "https://files.catbox.moe/lkdqdz.jpg",
    "https://files.catbox.moe/v6q08s.jpg",
    # ADD MORE IMAGES ASS YOU WANT
]

# IMGBB API KEY
IMGBB_API_KEY = "593edb35922f7a2c904ec752e2416d63"

# CHARA CHANNEL ID
CHARA_CHANNEL_ID = -1001234567890  

# OWNER ID
OWNER_ID = 123456789  

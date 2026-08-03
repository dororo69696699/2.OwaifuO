import os

API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8988622858:AAHamrsZ_mCiTB4L950B7k7Y8QApzcWPDRc")
MONGO_URL = os.getenv(
    "MONGO_URL",
    ""
)

# Card System Configurations
DEFAULT_SPAWN_LIMIT = int(os.getenv("DEFAULT_SPAWN_LIMIT", "100"))

SPAWN_TIMEOUT = int(os.getenv("SPAWN_TIMEOUT", "300"))  # 5 minutes in seconds

TRADE_TIMEOUT = int(os.getenv("TRADE_TIMEOUT", "600"))  # 10 minutes

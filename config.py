import os

# ==============================
# Telegram API
# ==============================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


# ==============================
# MongoDB
# ==============================

MONGO_URI = os.getenv("MONGO_URI")


# ==============================
# Bot Tokens
# ==============================

STARTUP_BOT_TOKEN = os.getenv("STARTUP_BOT_TOKEN")
APPROVAL_BOT_TOKEN = os.getenv("APPROVAL_BOT_TOKEN")
CONTROL_BOT_TOKEN = os.getenv("CONTROL_BOT_TOKEN")


# ==============================
# Owner & Admin
# ==============================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "").split() if x]


# ==============================
# Sessions
# ==============================

SESSION_FOLDER = "sessions"


# ==============================
# Verification system
# ==============================

VERIFY_CODES = {}

LOGIN_EXPIRY_SECONDS = 259200


# ==============================
# Auto Promo
# ==============================

DEFAULT_PROMO_TIME = 600


# ==============================
# Bots usernames
# ==============================

STARTUP_BOT_USERNAME = os.getenv("STARTUP_BOT_USERNAME")
APPROVAL_BOT_USERNAME = os.getenv("APPROVAL_BOT_USERNAME")
CONTROL_BOT_USERNAME = os.getenv("CONTROL_BOT_USERNAME")

from motor.motor_asyncio import AsyncIOMotorClient
import time
import config
import asyncio
from datetime import datetime, timedelta

# MongoDB connection
mongo = AsyncIOMotorClient(config.MONGO_URI)
db = mongo["userbot_system"]

users_db = db["users"]
admins_db = db["admins"]
autopromo_db = db["autopromo"]

# ----------------------
# USER FUNCTIONS
# ----------------------
async def add_user(user_id, username, phone, session):
    data = {
        "user_id": user_id,
        "username": username,
        "phone": phone,
        "session": session,
        "approved": False,
        "login_time": int(time.time())
    }
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )

async def approve_user(user_id):
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"approved": True, "login_time": int(time.time())}}
    )

async def is_approved(user_id):
    user = await users_db.find_one({"user_id": user_id})
    if user and user.get("approved"):
        return True
    return False

async def remove_user(user_id):
    await users_db.delete_one({"user_id": user_id})

async def get_all_users():
    users = []
    async for user in users_db.find():
        users.append(user)
    return users

# ----------------------
# ADMIN FUNCTIONS
# ----------------------
async def add_admin(user_id, username):
    data = {"user_id": user_id, "username": username}
    await admins_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )

async def is_admin(user_id):
    admin = await admins_db.find_one({"user_id": user_id})
    return admin is not None

# ----------------------
# AUTOPROMO FUNCTIONS
# ----------------------
async def save_autopromo(user_id, text, time_delay):
    data = {"user_id": user_id, "text": text, "time": time_delay}
    await autopromo_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )

async def get_autopromo(user_id):
    data = await autopromo_db.find_one({"user_id": user_id})
    return data

# ----------------------
# AUTO-EXPIRE TASK
# ----------------------
async def remove_expired_users():
    """Automatically disapprove users older than 3 days."""
    now = int(time.time())
    expiry_seconds = config.LOGIN_EXPIRY_SECONDS  # 259200 = 3 days

    async for user in users_db.find({"approved": True}):
        if now - user.get("login_time", now) > expiry_seconds:
            await users_db.update_one(
                {"user_id": user["user_id"]},
                {"$set": {"approved": False}}
            )
            print(f"⏳ User {user['user_id']} auto-disapproved (3 days expired).")

# Run background task in Control Bot
async def start_auto_expire_task():
    while True:
        try:
            await remove_expired_users()
        except Exception as e:
            print(f"❌ Error in auto-expire: {str(e)}")
        await asyncio.sleep(3600)  # check every hour

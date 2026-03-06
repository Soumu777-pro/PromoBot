from motor.motor_asyncio import AsyncIOMotorClient
import time
import config

# MongoDB connection
mongo = AsyncIOMotorClient(config.MONGO_URI)

db = mongo["userbot_system"]

users_db = db["users"]
admins_db = db["admins"]
autopromo_db = db["autopromo"]


# ADD USER
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


# APPROVE USER
async def approve_user(user_id):
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"approved": True}}
    )


# CHECK APPROVED
async def is_approved(user_id):
    user = await users_db.find_one({"user_id": user_id})

    if user and user.get("approved"):
        return True
    return False


# ADD ADMIN
async def add_admin(user_id, username):
    data = {
        "user_id": user_id,
        "username": username
    }

    await admins_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )


# CHECK ADMIN
async def is_admin(user_id):
    admin = await admins_db.find_one({"user_id": user_id})

    if admin:
        return True
    return False


# SAVE AUTOPROMO
async def save_autopromo(user_id, text, time_delay):
    data = {
        "user_id": user_id,
        "text": text,
        "time": time_delay
    }

    await autopromo_db.update_one(
        {"user_id": user_id},
        {"$set": data},
        upsert=True
    )


# GET AUTOPROMO
async def get_autopromo(user_id):
    data = await autopromo_db.find_one({"user_id": user_id})
    return data


# REMOVE USER
async def remove_user(user_id):
    await users_db.delete_one({"user_id": user_id})


# GET ALL USERS
async def get_all_users():
    users = []
    async for user in users_db.find():
        users.append(user)
    return users

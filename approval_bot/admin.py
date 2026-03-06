from pyrogram import Client, filters
import config

Temporary storage (later database.py se connect kar sakte ho)

pending_users = {}
approved_users = {}

OWNER CHECK

def is_owner(user_id: int) -> bool:
return user_id == config.OWNER_ID

APPROVE COMMAND

@Client.on_message(filters.command("approve") & filters.private)
async def approve_user(client, message):

if not is_owner(message.from_user.id):
    await message.reply_text("❌ Only owner can approve users.")
    return

if len(message.command) < 2:
    await message.reply_text("Usage: /approve user_id")
    return

try:
    user_id = int(message.command[1])
except ValueError:
    await message.reply_text("❌ Invalid user ID.")
    return

approved_users[user_id] = True
pending_users.pop(user_id, None)

await message.reply_text(f"✅ User {user_id} approved successfully.")

REJECT COMMAND

@Client.on_message(filters.command("reject") & filters.private)
async def reject_user(client, message):

if not is_owner(message.from_user.id):
    await message.reply_text("❌ Only owner can reject users.")
    return

if len(message.command) < 2:
    await message.reply_text("Usage: /reject user_id")
    return

try:
    user_id = int(message.command[1])
except ValueError:
    await message.reply_text("❌ Invalid user ID.")
    return

pending_users.pop(user_id, None)

await message.reply_text(f"❌ User {user_id} rejected.")

LIST APPROVED USERS

@Client.on_message(filters.command("list") & filters.private)
async def list_users(client, message):

if not is_owner(message.from_user.id):
    return

if not approved_users:
    await message.reply_text("⚠️ No approved users yet.")
    return

users = "\n".join(str(uid) for uid in approved_users)

await message.reply_text(
    f"✅ Approved Users:\n\n{users}"
)

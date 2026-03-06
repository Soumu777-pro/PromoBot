from pyrogram import Client, filters
import config

Pending users storage (temporary, later database.py se connect kar sakte ho)

pending_users = {}

USER REQUEST APPROVAL

@Client.on_message(filters.command("add") & filters.private)
async def request_access(client, message):

user = message.from_user
user_id = user.id
username = user.username if user.username else "No Username"

# Check if already requested
if user_id in pending_users:
    await message.reply_text(
        "⏳ Your request is already pending approval."
    )
    return

# Save request
pending_users[user_id] = {
    "username": username
}

# Reply to user
await message.reply_text(
    "✅ Your request has been sent to the admin.\n"
    "Please wait for approval."
)

# Notify owner
owner_message = (
    f"📩 New Userbot Access Request\n\n"
    f"👤 Name: {user.first_name}\n"
    f"🔗 Username: @{username}\n"
    f"🆔 User ID: {user_id}\n\n"
    f"Approve using:\n"
    f"/approve {user_id}"
)

await client.send_message(
    config.OWNER_ID,
    owner_message
)

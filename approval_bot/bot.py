from pyrogram import Client
import config

app = Client(
"approval-bot",
api_id=config.API_ID,
api_hash=config.API_HASH,
bot_token=config.APPROVAL_BOT_TOKEN
)

print("Approval Bot Running...")

app.run()

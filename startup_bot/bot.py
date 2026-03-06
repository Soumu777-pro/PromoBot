from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

# BOT CLIENT
bot = Client(
    "startup-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


# START COMMAND
@bot.on_message(filters.command("start"))
async def start_cmd(client, message):

    text = f"""
**Hey, this is Dhruv's Ultra Userbot 🤖**

This bot lets you control your Telegram userbot with many common and unique features.

Steps to use:

1️⃣ Generate your **String Session**
2️⃣ Send it here to login
3️⃣ Get approval from admin
4️⃣ Control your userbot

⚡ Login time: **3 days**

Click below to generate your string session.
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Generate String Session",
                    url="https://t.me/ArchStringBot"
                )
            ],
            [
                InlineKeyboardButton(
                    "Go to Approval Bot",
                    url=f"https://t.me/{config.APPROVAL_BOT_USERNAME}"
                )
            ]
        ]
    )

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )


# STRING SESSION RECEIVE
@bot.on_message(filters.text & ~filters.command(["start"]))
async def get_string(client, message):

    string = message.text.strip()

    if len(string) < 50:
        await message.reply_text("❌ Invalid String Session.")
        return

    await message.reply_text(
        "✅ String session received.\n\n"
        "⏳ Waiting for admin approval.\n"
        f"Please go to @{config.APPROVAL_BOT_USERNAME}"
    )


print("Startup Bot Running...")

bot.run()

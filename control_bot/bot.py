from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from userbots.manager import UserbotManager
import asyncio

# -------------------------
# Control Bot Client
# -------------------------
bot = Client(
    "control-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.CONTROL_BOT_TOKEN
)

# Userbot Manager instance
userbot_manager = UserbotManager(config.SESSION_FOLDER)

# -------------------------
# /start command - show available sessions
# -------------------------
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = (
        "**Control Bot Panel**\n\n"
        "✅ Select your logged-in userbot account to manage commands."
    )

    buttons = []
    sessions = userbot_manager.list_sessions()
    if not sessions:
        buttons = [[InlineKeyboardButton("No active userbots", callback_data="none")]]
    else:
        for sess in sessions:
            buttons.append([InlineKeyboardButton(sess, callback_data=f"select_{sess}")])

    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(text, reply_markup=reply_markup)


# -------------------------
# Callback Query - session selection
# -------------------------
@bot.on_callback_query()
async def cb_handler(client, callback_query):
    data = callback_query.data

    if data.startswith("select_"):
        session_name = data.split("_", 1)[1]
        userbot_manager.set_current_user(callback_query.from_user.id, session_name)
        await callback_query.answer(f"Selected userbot: {session_name}")
        await callback_query.message.edit(
            f"✅ Userbot `{session_name}` selected.\n"
            "You can now use commands like /promo, /autopromo, /bio, /send"
        )


# -------------------------
# /promo - send a broadcast via selected userbot
# -------------------------
@bot.on_message(filters.command("promo") & filters.private)
async def promo_cmd(client, message):
    user_id = message.from_user.id
    session_name = userbot_manager.get_current_user(user_id)

    if not session_name:
        await message.reply_text("❌ Select a userbot first with /start.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: /promo <text>")
        return

    text = " ".join(message.command[1:])
    result = await userbot_manager.send_promo(session_name, text)
    await message.reply_text(result)


# -------------------------
# /bio - update bio of selected userbot
# -------------------------
@bot.on_message(filters.command("bio") & filters.private)
async def bio_cmd(client, message):
    user_id = message.from_user.id
    session_name = userbot_manager.get_current_user(user_id)

    if not session_name:
        await message.reply_text("❌ Select a userbot first with /start.")
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: /bio <text>")
        return

    text = " ".join(message.command[1:])
    result = await userbot_manager.change_bio(session_name, text)
    await message.reply_text(result)


# -------------------------
# /send - send /start to @spambot N times
# -------------------------
@bot.on_message(filters.command("send") & filters.private)
async def send_cmd(client, message):
    user_id = message.from_user.id
    session_name = userbot_manager.get_current_user(user_id)

    if not session_name:
        await message.reply_text("❌ Select a userbot first with /start.")
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        await message.reply_text("Usage: /send <count>")
        return

    count = int(message.command[1])
    result = await userbot_manager.send_start_to_spambot(session_name, count)
    await message.reply_text(result)


# -------------------------
# /autopromo - start auto broadcast every X seconds
# -------------------------
@bot.on_message(filters.command("autopromo") & filters.private)
async def autopromo_cmd(client, message):
    user_id = message.from_user.id
    session_name = userbot_manager.get_current_user(user_id)

    if not session_name:
        await message.reply_text("❌ Select a userbot first with /start.")
        return

    if len(message.command) != 3:
        await message.reply_text("Usage: /autopromo <text> <interval_seconds>")
        return

    text = message.command[1]
    try:
        interval = int(message.command[2])
    except:
        await message.reply_text("❌ Interval must be a number in seconds.")
        return

    await message.reply_text(f"✅ Auto promo started every {interval} seconds.")
    asyncio.create_task(userbot_manager.autopromo(session_name, text, interval))


# -------------------------
# Run the bot
# -------------------------
print("Control Bot Running...")

bot.run()

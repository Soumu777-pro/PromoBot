# userbots/manager.py
import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import SESSION_FOLDER

# Ensure sessions folder exists
os.makedirs(SESSION_FOLDER, exist_ok=True)

class UserbotManager:
    def __init__(self, folder=SESSION_FOLDER):
        self.folder = folder
        self.sessions = {}  # user_id -> session_name
        self.clients = {}   # session_name -> TelegramClient

    # ----------------------
    # Session Management
    # ----------------------
    def list_sessions(self):
        """Return list of available session names."""
        return [f.replace(".session", "") for f in os.listdir(self.folder) if f.endswith(".session")]

    def set_current_user(self, user_id, session_name):
        """Set the selected session for a user."""
        self.sessions[user_id] = session_name

    def get_current_user(self, user_id):
        """Get the selected session for a user."""
        return self.sessions.get(user_id, None)

    # ----------------------
    # Client Loader
    # ----------------------
    async def get_client(self, session_name):
        """Return a Telethon client for a session, create if not exists."""
        if session_name in self.clients:
            return self.clients[session_name]

        session_path = os.path.join(self.folder, f"{session_name}.session")
        client = TelegramClient(StringSession(session_name), int(os.getenv("API_ID")), os.getenv("API_HASH"))
        await client.start()
        self.clients[session_name] = client
        return client

    # ----------------------
    # Commands
    # ----------------------
    async def send_promo(self, session_name, text):
        """Send text to all chats of the userbot."""
        client = await self.get_client(session_name)
        count = 0
        async for dialog in client.iter_dialogs():
            try:
                await client.send_message(dialog.id, text)
                count += 1
            except Exception:
                continue
        return f"✅ Promo sent to {count} chats/groups."

    async def change_bio(self, session_name, text):
        """Change userbot's bio."""
        client = await self.get_client(session_name)
        try:
            await client(UpdateProfileRequest(about=text))
            return "✅ Bio updated successfully."
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def send_start_to_spambot(self, session_name, count):
        """Send /start to @spambot multiple times."""
        client = await self.get_client(session_name)
        try:
            for _ in range(count):
                await client.send_message("@spambot", "/start")
                await asyncio.sleep(1)
            return f"✅ /start sent {count} times."
        except Exception as e:
            return f"❌ Error: {str(e)}"

    async def autopromo(self, session_name, text, interval):
        """Automatically broadcast promo every interval seconds."""
        client = await self.get_client(session_name)
        while True:
            async for dialog in client.iter_dialogs():
                try:
                    await client.send_message(dialog.id, text)
                except Exception:
                    continue
            await asyncio.sleep(interval)

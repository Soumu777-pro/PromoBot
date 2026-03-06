import sqlite3
import time

DB_NAME = "userbot.db"

def get_db():
return sqlite3.connect(DB_NAME)

def init_db():
conn = get_db()
cur = conn.cursor()

# users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    phone TEXT,
    session TEXT,
    approved INTEGER DEFAULT 0,
    login_time INTEGER
)
""")

# admins table
cur.execute("""
CREATE TABLE IF NOT EXISTS admins (
    user_id INTEGER PRIMARY KEY,
    username TEXT
)
""")

# autopromo table
cur.execute("""
CREATE TABLE IF NOT EXISTS autopromo (
    user_id INTEGER,
    text TEXT,
    time INTEGER
)
""")

conn.commit()
conn.close()

add user

def add_user(user_id, username, phone, session):
conn = get_db()
cur = conn.cursor()

cur.execute(
    "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?)",
    (user_id, username, phone, session, 0, int(time.time()))
)

conn.commit()
conn.close()

approve user

def approve_user(user_id):
conn = get_db()
cur = conn.cursor()

cur.execute("UPDATE users SET approved=1 WHERE user_id=?", (user_id,))

conn.commit()
conn.close()

check approval

def is_approved(user_id):
conn = get_db()
cur = conn.cursor()

cur.execute("SELECT approved FROM users WHERE user_id=?", (user_id,))
data = cur.fetchone()

conn.close()

if data and data[0] == 1:
    return True
return False

add admin

def add_admin(user_id, username):
conn = get_db()
cur = conn.cursor()

cur.execute(
    "INSERT OR REPLACE INTO admins VALUES (?, ?)",
    (user_id, username)
)

conn.commit()
conn.close()

check admin

def is_admin(user_id):
conn = get_db()
cur = conn.cursor()

cur.execute("SELECT * FROM admins WHERE user_id=?", (user_id,))
data = cur.fetchone()

conn.close()

return bool(data)

remove expired logins (3 days)

def remove_expired(expiry_seconds):
conn = get_db()
cur = conn.cursor()

now = int(time.time())
cur.execute("DELETE FROM users WHERE ? - login_time > ?", (now, expiry_seconds))

conn.commit()
conn.close()

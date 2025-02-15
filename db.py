import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def setup_db():
    """Bazani yaratish"""
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS invites (
            user_id TEXT PRIMARY KEY,
            invite_link TEXT NOT NULL
        )
    """)
    await conn.close()

async def get_invite(user_id):
    """Foydalanuvchining taklif havolasini olish"""
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow("SELECT invite_link FROM invites WHERE user_id = $1", user_id)
    await conn.close()
    return row['invite_link'] if row else None

async def save_invite(user_id, invite_link):
    """Foydalanuvchining taklif havolasini saqlash"""
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("INSERT INTO invites (user_id, invite_link) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET invite_link = $2", user_id, invite_link)
    await conn.close()
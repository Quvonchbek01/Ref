import asyncio
import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatInviteLink
from aiogram.filters import Command  
from dotenv import load_dotenv
import os  

# .env dan TOKEN yuklash
load_dotenv()
TOKEN = os.getenv("TOKEN")

CHANNEL_ID = -1002447889063  
bot = Bot(token=TOKEN)
dp = Dispatcher()

DB_FILE = "invites.db"

# **1. SQL jadvalini yaratish (agar mavjud bo‘lmasa)**
def setup_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invites (
            user_id TEXT PRIMARY KEY,
            invite_link TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# **2. Foydalanuvchining taklif havolasi mavjudligini tekshirish**
def get_invite(user_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT invite_link FROM invites WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None  # **Bazadan havolani qaytarish**

# **3. Yangi taklif havolasini saqlash**
def save_invite(user_id: str, invite_link: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO invites (user_id, invite_link) VALUES (?, ?)", (user_id, invite_link))
    conn.commit()
    conn.close()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Assalomu alaykum!\nTaklif havolasi olish uchun +kurs deb yozing.")

@dp.message()
async def kurs_handler(message: Message):
    if message.text.strip().lower() == "+kurs":
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        invite_link = get_invite(user_id)  # **Bazadan havolani tekshiramiz**
        if invite_link:
            await message.answer(f"✅ Sizga allaqachon taklif havolasi berilgan!\n🔗 {invite_link}")
        else:
            try:
                new_invite: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=6,
                    name=f"{user_name} ref"
                )
                save_invite(user_id, new_invite.invite_link)  # **Bazaga saqlaymiz**

                await message.answer(f"🎉 Taklif havolasi yaratildi!\n📌 {user_name} ref:\n🔗 {new_invite.invite_link}")
            except Exception as e:
                await message.answer("❌ Kechirasiz, taklif havolasini yaratib bo‘lmadi.\nAdmin bilan bog‘laning: @xlertuzb")
                logging.error(f"Xatolik: {e}")

async def main():
    setup_db()  # **Bot ishga tushganda bazani tayyorlaymiz**
    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())  
    except RuntimeError:  
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
import asyncio
import logging
import json
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatInviteLink
from aiogram.filters import Command  
from dotenv import load_dotenv  # .env fayldan yuklash uchun

# .env faylini yuklash
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002447889063

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

INVITES_FILE = "invites.json"

def load_invites():
    try:
        with open(INVITES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_invites():
    with open(INVITES_FILE, "w", encoding="utf-8") as file:
        json.dump(user_invites, file, indent=4)

user_invites = load_invites()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Assalomu alaykum!\nTaklif havolasi olish uchun <b>+kurs</b> deb yozing.")

@dp.message()
async def kurs_handler(message: Message):
    if message.text.strip().lower() == "+kurs":
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        if user_id in user_invites:
            await message.answer(f"✅ Sizga allaqachon taklif havolasi berilgan!\n"
                                 f"🔗 Taklif havolangiz: {user_invites[user_id]}")
        else:
            try:
                invite_link: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=6,
                    name=f"{user_name} ref"
                )
                user_invites[user_id] = invite_link.invite_link
                save_invites()

                await message.answer(f"🎉 Taklif havolasi yaratildi!\n"
                                     f"📌 <b>{user_name} ref</b> havolangiz:\n"
                                     f"🔗 {invite_link.invite_link}")
            except Exception as e:
                await message.answer("❌ Kechirasiz, taklif havolasini yaratib bo‘lmadi.\n"
                                     "Admin bilan bog‘laning: @xlertuzb")
                logging.error(f"Xatolik: {e}")

async def main():
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

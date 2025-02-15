import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ChatInviteLink
from aiogram.filters import Command
from dotenv import load_dotenv
from db import setup_db, get_invite, save_invite  # **Yangi db.py faylidan import qilamiz**

# **.env dan TOKEN yuklash**
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002447889063

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Assalomu alaykum!\nTaklif havolasi olish uchun +kurs deb yozing.")

@dp.message()
async def kurs_handler(message: Message):
    if message.text.strip().lower() == "+kurs":
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        invite_link = await get_invite(user_id)  # **Bazadan tekshiramiz**
        if invite_link:
            await message.answer(f"✅ Sizga allaqachon taklif havolasi berilgan!\n🔗 {invite_link}")
        else:
            try:
                new_invite: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=6,
                    name=f"{user_name} ref"
                )
                await save_invite(user_id, new_invite.invite_link)  # **Bazaga saqlaymiz**

                await message.answer(f"🎉 Taklif havolasi yaratildi!\n📌 {user_name} ref:\n🔗 {new_invite.invite_link}")
            except Exception as e:
                await message.answer("❌ Kechirasiz, taklif havolasini yaratib bo‘lmadi.\nAdmin bilan bog‘laning: @xlertuzb")
                logging.error(f"Xatolik: {e}")

async def main():
    await setup_db()  # **PostgreSQL bazani yaratamiz**
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
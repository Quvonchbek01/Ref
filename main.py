import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update, ChatInviteLink
from aiogram.filters import Command
from dotenv import load_dotenv
from aiohttp import web
from aiogram import types

# **.env faylni yuklash**
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002350982567

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Xotirada saqlanadigan dictionary (foydalanuvchilar va havolalar)
invites = {}

@dp.message(Command("start", "hack", "crack"))
async def start_cmd(message):
    await message.answer(f"👋 Welcome, {message.from_user.first_name}!\nSolve the following riddle and join Cracking World!\nWhat is something that is both valuable and worthless at the same time?")

@dp.message()
async def kurs_handler(message):
    if message.text.strip().lower() == "time":
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        # Xotiradagi invites dictdan foydalanuvchining havolasini olish
        invite_link = invites.get(user_id)

        if invite_link:
            # Agar foydalanuvchi havolasini oldin olgan bo'lsa
            await message.answer(f"✅You have already been given the link!\nLink: 🔗 {invite_link}")
        else:
            try:
                # Foydalanuvchiga yangi taklif havolasini yaratish
                new_invite: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=1,
                    name=f"{user_name}'s ref"
                )

                # Yangi havolani xotiraga saqlash
                invites[user_id] = new_invite.invite_link

                # Foydalanuvchiga taklif havolasini yuborish
                await message.answer(f"🎉 Congrats!\nYour link has been created.\n📌 {user_name}'s link:\n🔗 {new_invite.invite_link}")
            except Exception as e:
                # Xatolik yuzaga kelsa, foydalanuvchiga xabar berish
                await message.answer("❌ Maybe you are professional hacker (Bruh, it's error)\n : Please text me : @xlertuzb")
                logging.error(f"Xatolik: {e}")

async def on_startup():
    """Botni ishga tushirishdan avval kerakli dasturlarni ishga tushirish"""
    logging.info("Bot ishga tushirildi")

async def on_shutdown():
    """Botni o'chirish"""
    logging.info("Bot o'chirildi")

async def handle_ping(request):
    """UptimeRobot yoki boshqa xizmatlar uchun oddiy GET so‘rovini qo‘llab-quvvatlash"""
    return web.Response(text="Bot is running!", status=200)

def main():
    logging.basicConfig(level=logging.INFO)

    # **AIOHTTP web-serverni yaratamiz**
    app = web.Application()
    app.router.add_get("/", handle_ping)  # GET so‘rov uchun, UptimeRobot va brauzer tekshiruvi uchun

    # **Botni pollingga o'tkazish**
    dp.start_polling(bot, on_startup=[on_startup], on_shutdown=[on_shutdown])

if __name__ == "__main__":
    main()

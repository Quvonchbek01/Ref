import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update, ChatInviteLink
from aiogram.filters import Command
from dotenv import load_dotenv
from aiohttp import web
from aiogram.webhook.aiohttp_server import setup_application
import asyncio

# **.env faylni yuklash**
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002350982567
BASE_URL = os.getenv("BASE_URL")  # Webhook uchun Render’dan olingan domen
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

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
            await message.answer(f"✅ You have already been given the link!\n🔗Link: {invite_link}")
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

async def handle_request(request):
    """Webhook orqali so‘rovlarni qabul qilish"""
    update = Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()

async def handle_ping(request):
    """UptimeRobot yoki boshqa xizmatlar uchun oddiy GET so‘rovini qo‘llab-quvvatlash"""
    return web.Response(text="Bot is running!", status=200)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

def main():
    logging.basicConfig(level=logging.INFO)

    # **AIOHTTP web-serverni yaratamiz**
    app = web.Application()
    setup_application(app, bot)  # Botni AIOHTTP serverga ulaymiz

    # Webhook uchun POST so‘rov
    app.router.add_post(WEBHOOK_PATH, handle_request)
    
    # GET so‘rov uchun, UptimeRobot va brauzer tekshiruvi uchun
    app.router.add_get("/", handle_ping)
    
    # Web serverni ishga tushurish
    web.run_app(app, host="0.0.0.0", port=443)

if __name__ == "__main__":
    main()

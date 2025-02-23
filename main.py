import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Update, ChatInviteLink
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from dotenv import load_dotenv
from db import setup_db, get_invite, save_invite  # Bazaga ulanish

# **.env faylni yuklash**
load_dotenv()
TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")  # Webhook uchun Render’dan olingan domen
CHANNEL_ID = -1002350982567
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start", "hack"))
async def start_cmd(message):
    await message.answer(f"👋 Welcome, {message.from_user.first.name}!\n Solve the following riddle and join Cracking World!\nWhat is something that is both valuable and worthless at the same time?")

@dp.message()
async def data_handler(message):
    if message.text.strip().lower() == "vaqt" or message.text.strip().lower() == "time"
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        invite_link = await get_invite(user_id)  # **Bazadan tekshiramiz**
        if invite_link:
            await message.answer(f"Don't hack ! \nYou have already been given the link.\n🔗 {invite_link}")
        else:
            try:
                new_invite: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=1,
                    name=f"{user_name}'s link"
                )
                await save_invite(user_id, new_invite.invite_link)  # **Bazaga saqlaymiz**

                await message.answer(f"🎉 Congrats! You got it right.\nLink has been created!\n📌 {user_name} ref:\n🔗 {new_invite.invite_link}")
            except Exception as e:
                await message.answer("❌ Error.\nPlease text me: @xlertuzb")
                logging.error(f"Error: {e}")

async def on_startup():
    """Webhookni o‘rnatish va bazani yaratish"""
    await setup_db()  # **PostgreSQL bazani yaratamiz**
    await bot.set_webhook(WEBHOOK_URL)  # **Telegram API webhook'ni sozlash**

async def on_shutdown():
    """Webhookni o‘chirish"""
    await bot.delete_webhook()

async def handle_request(request):
    """Telegram webhook so‘rovlarini qabul qilish"""
    update = Update(**await request.json())
    await dp.feed_update(bot, update)
    return web.Response()

async def handle_ping(request):
    """UptimeRobot yoki boshqa xizmatlar uchun oddiy GET so‘rovini qo‘llab-quvvatlash"""
    return web.Response(text="Bot is running!", status=200)

def main():
    logging.basicConfig(level=logging.INFO)

    # **AIOHTTP web-serverni yaratamiz**
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_request)  # Webhook uchun POST so‘rov
    app.router.add_get("/", handle_ping)  # GET so‘rov uchun, UptimeRobot va brauzer tekshiruvi uchun

    setup_application(app, dp, on_startup=[on_startup], on_shutdown=[on_shutdown])

    # **Webhook serverni ishga tushirish**
    web.run_app(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()

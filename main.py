import os
from aiogram import Bot, Dispatcher
from aiogram.types import ChatInviteLink
from aiogram.filters import Command
from dotenv import load_dotenv
from db import get_invite, save_invite  # Bazaga ulanish

# .env faylni yuklash
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002350982567

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start", "hack"))
async def start_cmd(message):
    await message.answer(f"👋 Welcome, {message.from_user.first_name}!\nSolve the following riddle and join Cracking World!\nWhat is something that is both valuable and worthless at the same time?")

@dp.message()
async def kurs_handler(message):
    if message.text.strip().lower() in ["vaqt", "time"]:
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name

        invite_link = await get_invite(user_id)  # Bazadan tekshiramiz
        if invite_link:
            await message.answer(f"Don't hack! \nYou have already been given the link.\n🔗 {invite_link}")
        else:
            try:
                new_invite: ChatInviteLink = await bot.create_chat_invite_link(
                    chat_id=CHANNEL_ID,
                    member_limit=1,
                    name=f"{user_name}'s link"
                )
                await save_invite(user_id, new_invite.invite_link)  # Bazaga saqlaymiz
                await message.answer(f"🎉 Congrats! You got it right.\nLink has been created!\n📌 {user_name} ref:\n🔗 {new_invite.invite_link}")
            except Exception:
                await message.answer("❌ Error.\nPlease text me: @xlertuzb")

async def on_start():
    while True:  # Pollingni cheksiz davom ettirish
        try:
            await dp.start_polling(bot)
        except Exception:
            await asyncio.sleep(5)  # Xato yuzaga kelganda kutib turing va qayta urinish

if __name__ == "__main__":
    asyncio.run(on_start())

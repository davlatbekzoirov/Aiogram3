from data.config import ADMINS, BOT_TOKEN
from aiogram import Bot, Dispatcher

bot = Bot(token=BOT_TOKEN)
async def on_startup_notify():
    for admin in ADMINS:
        await bot.send_message(chat_id='-1002061183513',text="✅Bot ishga tushirildi")

async def on_shutdown_notify():
    for admin in ADMINS:
        await bot.send_message(chat_id='-1002061183513', text="❌Bot to'xtatildi")
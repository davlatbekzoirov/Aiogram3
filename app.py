from aiogram import Dispatcher
from loader import *  # Yuqoridagi `loader` modulidan barcha narsalarni import qilamiz
import asyncio, handlers, middlewares, filters, utils  # Middleware, filtrlar, va qo'llanma qabulchilari uchun modullarni import qilamiz
from utils.notify_admins import *  # Administratorlarga bildirishnoma yuborish uchun funksiyalarni import qilamiz
from utils.set_bot_commands import set_default_commands  # Bot buyruqlarini sozlash uchun funksiya

async def main():
    dp.startup.register(on_startup_notify)  # Botni ishga tushirish jarayonida xabar yuborish uchun funktsiyani ro'yxatga qo'shamiz
    dp.shutdown.register(on_shutdown_notify)  # Botni to'xtatish jarayonida xabar yuborish uchun funktsiyani ro'yxatga qo'shamiz
    await set_default_commands(bot)  # Bot buyruqlarini standart buyruqlar bo'yicha sozlaymiz
    try:db.create_table_users()  # Foydalanuvchilar jadvalidini yaratish
    except Exception:pass
    try:db.create_table_audios()  # Audio jadvalidini yaratish
    except Exception:pass
    await dp.start_polling(bot)  # Botni polling rejimida ishga tushiramiz

if __name__ == '__main__':
    asyncio.run(main())  # Asinxron amallarni boshlash uchun `asyncio.run` funksiyasini ishga tushiramiz
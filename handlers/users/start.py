from aiogram import types
from aiogram.filters import CommandStart
from loader import dp, db, bot

@dp.message(CommandStart())
async def start_command(message: types.Message):
    # Foydalanuvchi to'liq ismini va telegram ID sini olish
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        # Foydalanuvchini ma'lumotlar bazasiga qo'shish
        db.add_user(full_name=full_name, telegram_id=telegram_id)
        # Foydalanuvchiga xush kelibsiz habarini yuborish
        await message.answer(text="Assalomu alaykum, botimizga hush kelibsiz")
    except:
        # Agar xato bo'lsa, xatolik haqida xabar yuborish
        await message.answer(text="Assalomu alaykum")

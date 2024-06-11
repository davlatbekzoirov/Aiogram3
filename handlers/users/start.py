from aiogram import types
from aiogram.filters import CommandStart
from loader import dp, db

@dp.message(CommandStart())
async def start_command(message: types.Message):
    try:
        db.add_user(telegram_id=message.from_user.id, full_name=message.from_user.username)
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")
    except Exception as e:
        await message.answer("Assalomu alaykum")

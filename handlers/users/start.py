from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp, db
from keyboards.default.build import hududlar_button

@dp.message(CommandStart())
async def start_command(message: types.Message):
    try:
        db.add_user(telegram_id=message.from_user.id, full_name=message.from_user.username)
        await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=hududlar_button)
    except Exception as e:
        await message.answer("Assalomu alaykum", reply_markup=hududlar_button)


# BQACAgIAAxkBAAIIuGZqhT3ZfRbrVAqWGa8a6X3iItjKAAKGbAAC2LngS9X15oIQ--JDNQQ
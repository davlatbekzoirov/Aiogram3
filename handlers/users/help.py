from aiogram import types
from aiogram.filters import Command
from loader import dp


@dp.message(Command('help'))
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")    
    await message.answer("\n".join(text))
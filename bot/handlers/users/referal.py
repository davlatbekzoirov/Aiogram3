from aiogram import types, F
from loader import dp
from utils.db_api.api import increase_user_points, get_user_points
from aiogram.fsm.context import FSMContext
from keyboards.default.referal import referal


@dp.message(F.text == 'Referal link')
async def referal_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    ref_link = f"https://t.me/navoiy_mahalla_bot?start={user_id}"

    if message.text == ref_link:
        await message.answer("Siz o'zingizning referal bo'la olmaysiz.", reply_markup=referal)
    else:
        increase_user_points(user_id, 1) 
        await message.answer(f'Sizning referal codingiz {ref_link}', reply_markup=referal)


@dp.message(F.text == 'Mening ballarim')
async def show_user_points(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    points = get_user_points(user_id)
    
    if points is not None:  # Handle the case where points might be 0
        await message.answer(f"Sizning ballaringiz: {points}", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Xoziorcha sizda ballar yo'q", reply_markup=types.ReplyKeyboardRemove())

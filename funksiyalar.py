from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from data import users, get_user_ball
from states import get_user_realy_name
from keyboards import main_menu

async def start_command_answer(message: Message, state: FSMContext):
    if message.text[7:].isdigit():
        if users.get(str(message.from_user.id)):
            if int(message.text[7:]) == message.from_user.id: await message.answer("Siz o'zingizga referal bo'la olmaysiz!")
            else: await message.answer("Siz botga oldin tashrif buyurgansiz va referal bo'la olmaysiz!")
        else:
            reffer_id =message.text[7:]
            users[str(message.from_user.id)] = {"reffer_id": reffer_id, 'flag': False}

            await state.set_state(get_user_realy_name.name)
            await message.answer("Menga haqiqiy ismingizni kiriting.")
    else:
        if users.get(str(message.from_user.id)):
            if users.get(str(message.from_user.id)).get("user_realy_name"):
                await message.answer("Asosiy menyudasiz!", reply_markup=main_menu)
            else:
                await message.answer("Ism-familyangizni kiriting.")
        else:
            users[str(message.from_user.id)] = {"reffer_id": None, 'flag': False}
            print(message.from_user.id)
            await state.set_state(get_user_realy_name.name)
            await message.answer("Menga haqiqiy ismingizni kiriting.")

async def get_user_realy_name_answer(message: Message, state: FSMContext):
    users[str(message.from_user.id)]["user_realy_name"] = message.text
    users[str(message.from_user.id)]["flag"] = True

    await message.answer(f"{message.text} sizni eslab qoldim.", reply_markup=main_menu)
    await state.clear()

async def get_ref_link_answer(message: Message, state: FSMContext):
    if users.get(str(message.from_user.id)):
        ref_link = f"https://t.me/openweather_map_bot?start={message.from_user.id}"
        await message.answer(f"Sizning referal havolangiz:\n\n{ref_link}")
    else:
        users[str(message.from_user.id)] = {"reffer_id": None, 'flag': False}
        print(message.from_user.id)
        await state.set_state(get_user_realy_name.name)
        await message.answer("Menga haqiqiy ismingizni kiriting.")

async def get_user_ball_answer(message: Message, state: FSMContext):
    if users.get(str(message.from_user.id)):
        user_ball = get_user_ball(str(message.from_user.id))
        await message.answer(f"Sizning ballingiz: {user_ball} ball")
    else:
        users[str(message.from_user.id)] = {"reffer_id": None, 'flag': False}
        print(message.from_user.id)
        await state.set_state(get_user_realy_name.name)
        await message.answer("Menga haqiqiy ismingizni kiriting.")

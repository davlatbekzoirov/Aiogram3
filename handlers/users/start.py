from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp, db, bot
from states.name import User
from aiogram.fsm.context import FSMContext
from .name import generate_image_with_text
from io import BytesIO

@dp.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum <b>{message.from_user.full_name}</b>.Botdan foydalanish uchun ismingizni kiriting", parse_mode='html')
    await state.set_state(User.name)

@dp.message(User.name)
async def image(msg: types.Message, state: FSMContext):
    await msg.answer('Endi rasm yuboring')
    name = msg.text
    await state.update_data(name=name)
    await state.set_state(User.photo)

@dp.message(F.photo, User.photo)
async def photo(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    photo = msg.photo[-1].file_id

    # * Fotosurat faylini olish
    file = await bot.get_file(photo)
    file_path = file.file_path

    photo_file = BytesIO()
    await bot.download_file(file_path, photo_file)
    photo_file.seek(0)

    # * Ism va fotosurat bilan rasm yarating
    photo = await generate_image_with_text(photo_file, name)

    # * Yaratilgan rasmni yuborish
    photo=types.input_file.BufferedInputFile(photo,filename=f"{name}.png")
    # ! Bu satr yaratilgan tasvirni oladi, uni BufferedInputFile ob'ektiga o'rab oladi va keyin uni foydalanuvchiga fotoxabar sifatida yuboradi.
    await msg.answer_photo(photo=photo)

    try:
        db.add_user(telegram_id=msg.from_user.id, full_name=name)
    except Exception as e:
        pass

    await state.clear()

@dp.message(User.photo)
async def photo_fake(msg: types.Message, state: FSMContext):
    await msg.answer('Iltimos rasm yuboring')
    await state.set_state(User.photo)
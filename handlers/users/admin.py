from loader import dp, db, bot
from filters.admin import IsBotAdminFilter  # adminlar uchun filtrni import qilamiz
from data.config import ADMINS  # adminlar ro'yxatini import qilamiz
from aiogram.types import Message
from keyboards.default import admin_keyboard
from aiogram.filters import Command
from states.reklama import Adverts, AudioState
from aiogram.fsm.context import FSMContext
import time
from aiogram import F
    
@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))  # `/admin` buyrug'ini qabul qilish uchun filtri ishlatamiz
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_keyboard.admin_button)  # admin menyusini yuboramiz

@dp.message(F.text == "Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))  # "Foydalanuvchilar soni" so'zini tekshiramiz
async def users_count(message: Message):
    counts = db.count_users()  # foydalanuvchilar sonini hisoblaymiz
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)  # foydalanuvchilarni hisoblarni javob qilib yuboramiz

@dp.message(F.text == "Reklama yuborish", IsBotAdminFilter(ADMINS))  # "Reklama yuborish" so'zini tekshiramiz
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)  # reklama yuborish holatiga o'tkazamiz
    await message.answer(text="Reklama yuborishingiz mumkin !")  # foydalanuvchiga yuborishning mumkinligini bildiramiz

@dp.message(Adverts.adverts)  # reklama yuborish holatini tekshiramiz
async def send_advert(message: Message, state: FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()  # barcha foydalanuvchilarni ID larini olish
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=from_chat_id, message_id=message_id)  # xabarni foydalanuvchiga yuboramiz
            count += 1
        except:
            pass
        time.sleep(0.5)  # foydalanuvchiga yuborishni qayta ishlatish uchun 0.5 saniyani qo'shamiz

    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")  # yuborilgan foydalanuvchilar sonini aytamiz
    await state.clear()  # holatni tozalaymiz

@dp.message(F.text == "audio qo'shish", IsBotAdminFilter(ADMINS))  # "audio qo'shish" so'zini tekshiramiz
async def auido_adds(message: Message, state: FSMContext):
    await message.answer("Audio nomini kiriting")  # foydalanuvchidan audioning nomini so'raymiz
    await state.set_state(AudioState.title)  # holatni audio nomini kiritish uchun o'rnating

@dp.message(F.text, AudioState.title)  # audioning nomini tekshiramiz
async def auido_title(message: Message, state: FSMContext): 
    await message.answer("Audio yuboring")  # audio yuborishni xabar qilamiz
    title = message.text
    await state.set_state(AudioState.voice_file_id)  # holatni audio faylini kiritish uchun o'rnating
    await state.update_data(title=title)  # ma'lumotlarni yangilaymiz

@dp.message(F.voice, AudioState.voice_file_id)  # audio faylini tekshiramiz
async def auido_voice(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    voice_file_id = message.voice.file_id
    db.add_audio(voice_file_id=voice_file_id, title=title)  # audio faylini ma'lumotlar bazasiga qo'shamiz

    await message.answer("Audio muvaffaqiyatli bazaga qo'shildi")  # ma'lumotlarni qo'shish haqida xabar yuboramiz
    await state.clear()  # holatni tozalaymiz

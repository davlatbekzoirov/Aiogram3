from loader import dp, db, bot
from filters.admin import IsBotAdminFilter  
from data.config import ADMINS 
from aiogram.types import Message
from keyboards.default.admins_keyboard import admin_button, plus
from aiogram.filters import Command
from states.reklama import Adverts, TM
from aiogram.fsm.context import FSMContext
import time
from aiogram import F
from keyboards.default.build import hududlar_button, mahalla_button_admin, HUDUDLAR, navoiy_shahar, zarafshon_shahar, gazgon_shahar, karmana_shahar, konimex_shahar, qiziltepa_shahar, nurota_shahar, tomdi_tumani, uchquduq_tumani, xaturchi_tumani, xatirchi_tumani
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove

# Admin buyrug'i uchun handler
@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))  
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_button)  

# Foydalanuvchilar sonini olish uchun handler
@dp.message(F.text == "Foydalanuvchilar soni", IsBotAdminFilter(ADMINS)) 
async def users_count(message: Message):
    counts = db.count_users() 
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)  

# Reklama yuborish uchun handler
@dp.message(F.text == "Reklama yuborish", IsBotAdminFilter(ADMINS))  
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)  
    await message.answer(text="Reklama yuborishingiz mumkin !") 

# Reklama yuborishni boshqarish
@dp.message(Adverts.adverts)  
async def send_advert(message: Message, state: FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=from_chat_id, message_id=message_id) 
            count += 1
        except:
            pass
        time.sleep(0.5) 

    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")  
    await state.clear()  

# Nomzod qo'shish jarayonini boshlash
@dp.message(F.text == 'Nomzod', IsBotAdminFilter(ADMINS))
async def nomzod(msg: Message, state: FSMContext):
    await msg.answer('Iltimos tuman yoki shaharni yozing: ', reply_markup=hududlar_button)
    await state.set_state(TM.tuman)

# Tuman tanlash uchun handler
@dp.message(F.text.in_(HUDUDLAR), TM.tuman, IsBotAdminFilter(ADMINS))
async def tuman(msg: Message, state: FSMContext):
    tuman = msg.text
    button = None
    if msg.text == "Navoiy shahri":
        button = mahalla_button_admin(navoiy_shahar)
    elif msg.text == "Karmana tumani":
        button = mahalla_button_admin(karmana_shahar)
    elif msg.text == "Konimex tumani":
        button = mahalla_button_admin(konimex_shahar)
    elif msg.text == "Navbahor tumani":
        button = mahalla_button_admin(navoiy_shahar)
    elif msg.text == "Nurota tumani":
        button = mahalla_button_admin(nurota_shahar)
    elif msg.text == "Qiziltepa tumani":
        button = mahalla_button_admin(qiziltepa_shahar)
    elif msg.text == "Tomdi tumani":
        button = mahalla_button_admin(tomdi_tumani)
    elif msg.text == "Uchquduq tumani":
        button = mahalla_button_admin(uchquduq_tumani)
    elif msg.text == "Xatirchi tumani-1":
        button = mahalla_button_admin(xaturchi_tumani)
    elif msg.text == "Xatirchi tumani-2":
        button = mahalla_button_admin(xatirchi_tumani)
    elif msg.text == "Zarafshon shahri":
        button = mahalla_button_admin(zarafshon_shahar)
    elif msg.text == "Gʻazgʻon tumani":
        button = mahalla_button_admin(gazgon_shahar)
        
    await state.update_data(tuman=tuman)

    if button:
        await state.set_state(TM.mahalla)
        await msg.answer('Mahallani kiriting:', reply_markup=button)
    else:
        await msg.answer("Mahalla tanlanmagan yoki noto'g'ri nom kiritildi.")
    await state.set_state(TM.mahalla)

# Mahalla tanlash uchun handler
@dp.message(F.text, TM.mahalla, IsBotAdminFilter(ADMINS))
async def mahalla(msg: Message, state: FSMContext):
    mahalla = msg.text
    await state.update_data(mahalla=mahalla)
    await msg.answer("Endi maktabingiz yoki bog'changizni qo'shing", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TM.ovoz)

# Maktab yoki bog'cha nomini kiritish
@dp.message(F.text, TM.ovoz, IsBotAdminFilter(ADMINS))
async def ovoz(msg: Message, state: FSMContext):
    ovoz = msg.text
    await state.update_data(ovoz=ovoz)
    await msg.answer("Endi nomzodlarni ismini qo'shing:  ")
    await state.set_state(TM.name)

# Nomzod ismini kiritish va qayta qo'shish imkoniyati
@dp.message(F.text, TM.name, IsBotAdminFilter(ADMINS))
async def process_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    tuman = data.get('tuman')
    mahalla = data.get('mahalla')
    ovoz = data.get('ovoz')
    
    if msg.text == "Qo'shish":
        await msg.answer('Yana nomzodlarni qo\'shishingiz mumkin: ', reply_markup=plus)
        await state.set_state(TM.name)
    
    elif msg.text == "Tugadi":
        name = data.get('name')
        summary_message = f"{tuman}\n{mahalla}\n{ovoz}\n{name}"
        await msg.answer(summary_message)

        try:
            db.add_candidate(
                telegram_id=msg.from_user.id,
                full_name=name,
                district=tuman,
                neighborhood=mahalla,
                vote_place=ovoz
            )
            await msg.answer("Nomzod muvaffaqiyatli qo'shildi")
        except Exception as e:
            await msg.answer(f"Xatolik yuz berdi: {str(e)}")
        finally:
            db.connection.close()  

        await state.clear() 
    
    else:
        await state.update_data(name=msg.text)
        await msg.answer(f"Sizning nomzodingiz {msg.text}:", reply_markup=plus)

# Reytinglarni ko'rsatish uchun handler
@dp.message(Command("rating"), IsBotAdminFilter(ADMINS))  
async def is_admin(message: Message):
    ratings = db.top_rating
    format_arg = []
    for rating in ratings:
        full_name = rating[2]
        district = rating[3]
        vote_place = rating[4]
        average_rating = rating[-1]

        if average_rating is None:
            average_rating_str = "Hozircha reytinglar yoʻq"
        else:
            average_rating_str = f"{average_rating}"

        format_arg.append(f"<b>{district}</b> -> <code>{vote_place}</code> -> {full_name} - O'rtacha reyting: {average_rating_str}")

    if not rating:
        await message.answer("Baholar mavjud emas.")
        return



    await message.answer("\n".join(format_arg), parse_mode='HTML')

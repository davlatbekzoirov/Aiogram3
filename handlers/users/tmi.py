from loader import dp, db
from aiogram.types import Message
from aiogram import F
from keyboards.default.build import (
    create_kinder_school_reply_markup, create_candidate_reply_markup, hududlar_button,
    mahalla_button, HUDUDLAR, navoiy_shahar, zarafshon_shahar, gazgon_shahar, 
    karmana_shahar, konimex_shahar, qiziltepa_shahar, nurota_shahar, 
    tomdi_tumani, uchquduq_tumani, xaturchi_tumani, xatirchi_tumani
)
from aiogram.fsm.context import FSMContext  
from states.reklama import Mahalla
from aiogram.filters import and_f

# "⬅️ Ortga" tugmasi uchun handler
@dp.message(F.text == "⬅️ Ortga")
async def back_button_handler(msg: Message, state: FSMContext):
    await msg.answer("Hududni tanlang: ", reply_markup=hududlar_button)

# Hudud tanlash uchun handler
@dp.message(F.text.in_(HUDUDLAR))
async def tuman_handler(msg: Message, state: FSMContext):
    await state.update_data(tuman=msg.text)
    button = None

    if msg.text == "Navoiy shahri":
        button = mahalla_button(navoiy_shahar)
    elif msg.text == "Karmana tumani":
        button = mahalla_button(karmana_shahar)
    elif msg.text == "Konimex tumani":
        button = mahalla_button(konimex_shahar)
    elif msg.text == "Navbahor tumani":
        button = mahalla_button(navoiy_shahar)
    elif msg.text == "Nurota tumani":
        button = mahalla_button(nurota_shahar)
    elif msg.text == "Qiziltepa tumani":
        button = mahalla_button(qiziltepa_shahar)
    elif msg.text == "Tomdi tumani":
        button = mahalla_button(tomdi_tumani)
    elif msg.text == "Uchquduq tumani":
        button = mahalla_button(uchquduq_tumani)
    elif msg.text == "Xatirchi tumani-1":
        button = mahalla_button(xaturchi_tumani)
    elif msg.text == "Xatirchi tumani-2":
        button = mahalla_button(xatirchi_tumani)
    elif msg.text == "Zarafshon shahri":
        button = mahalla_button(zarafshon_shahar)
    elif msg.text == "Gʻazgʻon tumani":
        button = mahalla_button(gazgon_shahar)

    if button:
        await state.set_state(Mahalla.mahalla)
        await msg.answer('Mahallani kiriting:', reply_markup=button)
    else:
        await msg.answer("Mahalla tanlanmagan yoki noto'g'ri nom kiritildi.")

# Mahalla tanlash uchun handler
@dp.message(Mahalla.mahalla)
async def process_mahalla(msg: Message, state: FSMContext):
    if msg.text == "⬅️ Ortga":
        await back_button_handler(msg, state)
        return
    
    try:
        data = await state.get_data()
        district = data.get('tuman')
        neighborhood = msg.text
        await state.update_data(neighborhood=neighborhood)

        # Muayyan joylashuvdagi bolalar bog'chalari ro'yxatini olish
        kinder_schools = db.get_kinder_schools_by_location(district, neighborhood)
        
        if kinder_schools:
            keyboard = create_kinder_school_reply_markup(kinder_schools)
            await msg.answer("Maktab yoki bolalar bog'chasini tanlang:", reply_markup=keyboard)
            await state.set_state(Mahalla.maktab)
        else:
            await msg.answer("Bu hududda maktab yoki bolalar bog'chasi topilmadi.")
    
    except Exception as e:
        print(f"Error in process_mahalla function: {e}")

# Maktab yoki bolalar bog'chasini tanlash uchun handler
@dp.message(Mahalla.maktab)
async def process_maktab(msg: Message, state: FSMContext):
    if msg.text == "⬅️ Ortga":
        await state.set_state(Mahalla.mahalla)
        await process_mahalla(msg, state)
        return

    try:
        data = await state.get_data()
        district = data.get('tuman')
        neighborhood = data.get('neighborhood')
        kinder_school = msg.text
        await state.update_data(kinder_school=kinder_school)

        # Muayyan joylashuvdagi nomzodlarni olish
        candidates = db.get_candidates_by_location(district, neighborhood, kinder_school)
        
        if candidates:
            keyboard = create_candidate_reply_markup(candidates)
            await msg.answer("Nomzodni tanlang:", reply_markup=keyboard)
            await state.set_state(Mahalla.nomzod)
        else:
            await msg.answer("Bu hududda nomzodlar topilmadi.")
    
    except Exception as e:
        print(f"Error in process_maktab function: {e}")

# Nomzodni tanlash uchun handler
@dp.message(Mahalla.nomzod)
async def process_nomzod(msg: Message, state: FSMContext):
    if msg.text == "⬅️ Ortga":
        await state.set_state(Mahalla.maktab)
        await process_maktab(msg, state)
        return
    
    candidate_info = msg.text.split(' (')[0]  
    candidate = db.select_candidate(full_name=candidate_info)

    if candidate:
        candidate_id = candidate[0]
        await state.update_data(candidate_id=candidate_id)

        # Nomzodning reytingini oshirish
        db.increment_candidate_score(candidate_id)

        await msg.answer(f"✅✅ Tabriklaymiz, siz tanlagan nomzod {candidate_info}ga 1 ball qo'shildi.")
    else:
        await msg.answer("Tanlangan nomzod mavjud emas. Iltimos, qaytadan tanlang.")

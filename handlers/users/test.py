from aiogram import types
from aiogram.filters import CommandStart, Command
from states.test import *
from loader import *
from aiogram.fsm.context import FSMContext
from keyboards.inline.test import *
import asyncio, sys, logging, tracemalloc
from .sertificat import *

tracemalloc.start()
correct_answers_count = 0

@dp.message(Command('test'))
async def enter_test(message: types.Message, state: FSMContext):
    await message.answer("""Kayfiyatlar qalay ;)
Xo'sh, hozir siz bor yo'g'i 11 dona test ishlaysiz, lekin shuning o'zi yetarli bo'ladi. Demak, testni boshlashdan avval tanishib olsak. Ism va familiyangizni Ism Familiya shaklida yozib jo'nating. Masalan:
Eshmatjon Toshmatov

Iltimos, ma'lumotni to'g'ri kiriting, ism va familiyangiz sertifikatingizga yoziladi.
""")
    await state.set_state(TestStates.fullname)

@dp.message(TestStates.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text

    await state.update_data({"name": fullname})

    msg = "0-savol\nPython asoschisi?"
    await message.answer(msg, reply_markup=question1)
    await state.set_state(TestStates.QUESTION_1)
    
@dp.callback_query(lambda query: query.data in ['linus_torvalds', 'bill_geyts', 'steven_houking', 'gvido_van_rosum'], TestStates.QUESTION_1)
async def answer_question1(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = "1-savol\nPython bu -"
    await call.message.answer(msg, reply_markup=question2)
    if call.data == 'gvido_van_rosum':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_2)
    
@dp.callback_query(lambda query: query.data in ['interpretatsion_til', 'kompliyatsion_til', 'ilon'], TestStates.QUESTION_2)
async def answer_question2(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = "2-savol\nyield qanday tur hosil qilishda qo'llaniladi?"
    await call.message.answer(msg, reply_markup=question3)
    if call.data == 'interpretatsion_til':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_3)

@dp.callback_query(lambda query: query.data in ['sikl', 'generator', 'iterator', 'string'], TestStates.QUESTION_3)
async def answer_question3(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """3-savol\nfayl ochishda "w" rejimidan qanday maqsadda foydalaniladi?"""
    await call.message.answer(msg, reply_markup=question4)
    if call.data == 'generator':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_4)

@dp.callback_query(lambda query: query.data in ['oqish', 'yozish', 'yozish_va_oqish', 'bunday_rejim_yoq'], TestStates.QUESTION_4)
async def answer_question4(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """4-savol
quyidagi ifodadan keyin "a" ning qiymati qanday bo'ladi:
a = [1, 2][1 > 2]"""
    await call.message.answer(msg, reply_markup=question5)
    if call.data == 'yozish':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_5)

@dp.callback_query(lambda query: query.data in ['dastur_xatolik_beradi', 'zero', 'first', 'second'], TestStates.QUESTION_5)
async def answer_question5(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """5-savol
dastur natijasi qanday:

silly_list=[i for i in range(2,9,2) if i%2]
print(silly_list)"""
    await call.message.answer(msg, reply_markup=question6)

    if call.data == 'zero':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_6)

@dp.callback_query(lambda query: query.data in ['tfs', 'tfsn', 'tfse', 'bosh'], TestStates.QUESTION_6)
async def answer_question6(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = "6-savol\nquyidagi dastur nechta qiymat chop etadi?"
    msg +="""\nprint([x**2 for x in range(1, 11)])"""
    await call.message.answer(msg, reply_markup=question7)

    if call.data == 'tfse':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_7)

@dp.callback_query(lambda query: query.data in ['five', 'one', 'ten1', 'question7'], TestStates.QUESTION_7)
async def answer_question7(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """7-savol
dastur natijasi qanday?

print("{1}{0}{1}".format("cad","abra"))"""
    await call.message.answer(msg, reply_markup=question8)
    if call.data == 'five':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_8)

@dp.callback_query(lambda query: query.data in ['cadabracad', 'dastur_xato_tuzilgan', 'cadcad', 'abracadabra'], TestStates.QUESTION_8)
async def answer_question8(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """8-savol
dastur natijasi qanday?

def return_integer() -> int:
  return "1"

print(return_integer() + "2")"""
    await call.message.answer(msg, reply_markup=question9)

    if call.data == 'abracadabra':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_9)

@dp.callback_query(lambda query: query.data in ['t', 'o', 'xatolik_kelib_chiqadi', 'tt'], TestStates.QUESTION_9)
async def answer_question9(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """9-savol
dastur nechta son chop etadi?

nums = list(range(10))
nums2 = list(range(15))
nums.extend(nums2)
print(set(nums))"""
    await call.message.answer(msg, reply_markup=question10)
    if call.data == 'xatolik_kelib_chiqadi':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_10)

@dp.callback_query(lambda query: query.data in ['ten', 'tf', 'of', 'question10'], TestStates.QUESTION_10)
async def answer_question10(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    msg = """10-savol
dastur natijasi qanday?

a,*b,c=1,2,3,4,5
print(b)"""
    await call.message.answer(msg, reply_markup=question11)
    if call.data == 'tf':
        correct_answers_count += 1

    await state.set_state(TestStates.QUESTION_11)
    
@dp.callback_query(lambda query: query.data in ['two', 'xatolik_kelib_chiqadi1', 'ttf', 'ttf1'], TestStates.QUESTION_11)
async def answer_question11(call: types.CallbackQuery, state: FSMContext):
    global correct_answers_count

    await call.message.delete()
    if call.data == 'xatolik_kelib_chiqadi1':
        correct_answers_count += 1

    data = await state.get_data()
    name = data.get("name")
    if correct_answers_count >= 8:
        await call.message.answer(f"Tabriklaymiz, siz testni yakunladingiz!\nSizning natijangiz: {correct_answers_count//11*100}%")
        photo = await sertificat(name)
        photo=types.input_file.BufferedInputFile(photo,filename="sertificate.png")
        await call.message.answer_photo(photo=photo)
        ans.add_user_answers(telegram_id=call.message.from_user.id, full_name=name, count=correct_answers_count)
        await bot.send_message(chat_id='-1002061183513', text=f"""
🗞 Foydalanuvchi: {name}
🔄 Natijasi: {correct_answers_count//11*100}
➖➖➖➖➖➖➖➖➖➖➖
🖐Jami: {ans.count_users()[0]}""")
        await state.clear()
    else:
        await call.message.answer(f"Siz testni yakunlay olmadingiz!\nSizning natijangiz: {correct_answers_count//11*100}%")
        await state.clear()

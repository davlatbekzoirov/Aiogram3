from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp
from keyboards.default.menu import main_menu
from utils.db_api.api import *
from aiogram.fsm.context import FSMContext
from states.reklama import Users
from keyboards.default.phonenum import phone
from keyboards.default.role import role
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.options import create_inline_keyboard
from keyboards.default.referal import referal

# Handler for the /start command
@dp.message(CommandStart())
async def start_command(message: types.Message, command: CommandStart, state: FSMContext):
    telegram_id = message.from_user.id
    args = command.args  

    if is_telegram_id_registered(telegram_id):
        await message.answer(
            text="Assalomu alaykum, siz avval bot-dan foydalangansiz iltimos quydagi menulardan birini tanlang", 
            reply_markup=main_menu
        )
    else:
        # Check if the user joined using a referral link
        if args:
            referrer_id = int(args)
            if referrer_id == telegram_id:
                await message.answer("Siz o'zingizning referal bo'la olmaysiz.", reply_markup=referal)
            else:
                # Increase referrer's points
                increase_user_points(referrer_id, 1)
                await message.answer("Sizning referalingiz orqali foydalanuvchi ro'yxatdan o'tdi. Sizga 1 ball qo'shildi.")
        
        # Store the new user in the database
        await message.answer("Assalomu alaykum, ismingizni kiriting.")
        await state.set_state(Users.first_name)
        
        # Create a new referral code for the new user
        create_referral_code(
            reffer_id=telegram_id,  # Use the user's Telegram ID as the referral ID
            user_realy_name=message.from_user.full_name,
            points=0,  # Default points or any initial value
            flag=False
        )

@dp.message(F.text == 'Referal link')
async def referal_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    ref_link = f"https://t.me/navoiy_mahalla_bot?start={user_id}"

    await message.answer(f"Sizning referal codingiz:\n\n{ref_link}", reply_markup=referal)

@dp.message(F.text == 'Mening ballarim')
async def show_user_points(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    points = get_user_points(user_id)
    
    if points is not None:
        await message.answer(f"Sizning ballaringiz: {points}", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Xozircha sizda ballar yo'q yoki sizga tegishli referal kodi topilmadi.", reply_markup=ReplyKeyboardRemove())


@dp.message(F.text == 'Role-ni tanlash')
async def select_role(message: types.Message, state: FSMContext):
    await message.answer("Siz abiturientmisiz yoki student, meyudan birini tanlang", reply_markup=role)
    await state.set_state(Users.role)


# Handler for receiving the first name
@dp.message(Users.first_name)
async def get_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await state.set_state(Users.phone_number)
    text = "Raqamingizni kiriting"
    await message.answer(text=text, reply_markup=phone)


# Handler for receiving the phone number (when contact is shared)
@dp.message(Users.phone_number, F.contact)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await state.set_state(Users.age)
    text = "Yoshingizni kiriting!"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


# Handler for receiving the phone number (when text is provided instead of contact)
@dp.message(Users.phone_number)
async def handle_invalid_phone_number(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, haqiqiy telefon raqamini yuboring yoki kontaktingizni tanlang.", reply_markup=phone)


# Handler for receiving the age
@dp.message(Users.age)
async def age(message: types.Message, state: FSMContext):
    age_text = message.text
    if not age_text.isdigit():
        await message.answer("Iltimos, yoshingizni raqam sifatida kiriting.")
        await state.set_state(Users.age)
        return
    
    age = int(age_text)
    await state.update_data(age=age)
    await state.set_state(Users.role)
    await message.answer("Siz abiturientmisiz yoki student, meyudan birini tanlang", reply_markup=role)


# Handler for receiving the role
@dp.message(Users.role)
async def role_func(message: types.Message, state: FSMContext):
    role = message.text.lower()
    valid_roles = ["abiturient", "student"]
    telegram_id = message.from_user.id


    if role not in valid_roles:
        await message.answer("Iltimos, haqiqiy rolni tanlang.")
        return

    data = await state.get_data()
    first_name = data.get('first_name')
    phone_number = data.get('phone_number')
    age = data.get('age')

    if is_telegram_id_registered(telegram_id):
        pass
    else:
        create_user(name=first_name, age=age, phone_number=phone_number, role=role, telegram_id=telegram_id)
    
    questions = fetch_questions(role)
    await state.update_data(questions=questions, current_question_index=0, score=0)

    if questions:
        first_question = questions[0]
        options = first_question.get('options', [])
        keyboard = create_inline_keyboard(options)
        await message.answer(f"Savol: {first_question['text']}", reply_markup=keyboard)
    else:
        await message.answer("Savollar topilmadi.", reply_markup=ReplyKeyboardRemove())

    await state.set_state(Users.selected_option)


# Handler for handling option selection from inline keyboard
@dp.callback_query(F.data.startswith("option_"))
# async def handle_option_selection(callback_query: types.CallbackQuery, state: FSMContext):
#     option_id = callback_query.data.split("_")[1]
#     user_id = callback_query.from_user.id

#     data = await state.get_data()
#     role = data.get('role')
#     questions = data.get('questions')
#     options = data.get('options')
#     current_question_index = data.get('current_question_index', 0)
#     user_responses = data.get('user_responses', {})
#     score = data.get('score', 0)

#     # Save the selected option
#     if role == "student":
#         create_student(user_id, option_id)
#     else:
#         create_applicant(user_id, option_id)

#     # Record user response
#     current_question = questions[current_question_index]
#     user_responses[current_question['id']] = option_id
#     await state.update_data(user_responses=user_responses)

#     # Check if the selected option is correct
#     correct_option_id = current_question.get('correct_option')
#     if correct_option_id:
#         correct_option = next((o for o in options if o['id'] == correct_option_id), None)
#         if correct_option and correct_option['id'] == option_id:
#             score += 1

#     # Move to the next question
#     current_question_index += 1
#     if current_question_index >= len(questions):
#         # Generate the final result message
#         result_message = f"Javobingiz uchun rahmat!\nSizning natijangiz: {score} ball\n\n"
#         for question_id, selected_option_id in user_responses.items():
#             try:
#                 question = next(q for q in questions if q['id'] == question_id)
#                 option = next(o for o in options if o['id'] == selected_option_id)
#                 result_message += f"{question['text']}: {option['text']}\n"
#             except StopIteration:
#                 pass
#         await callback_query.message.edit_text(result_message)
#         await state.clear()
#         return

#     # Handle the next question
#     if current_question_index < len(questions):
#         next_question = questions[current_question_index]

#         # Create a list of options for the current question
#         filtered_options = [o for o in options if o['question'] == next_question['id']]

#         # Check if we have options to display
#         if not filtered_options:
#             await callback_query.message.edit_text("Bu savol uchun hech qanday variant mavjud emas.")
#             await state.clear()
#             return

#         keyboard = create_inline_keyboard(filtered_options)
#         await callback_query.message.edit_text(f"Savol: {next_question['text']}", reply_markup=keyboard)

#         # Update state with the new index and score
#         await state.update_data(current_question_index=current_question_index, score=score)

#     await callback_query.answer()
async def handle_option_selection(callback_query: types.CallbackQuery, state: FSMContext):
    # Extract data from callback_query.data
    callback_data_parts = callback_query.data.split('_')
    selected_option = callback_data_parts[1]
    is_true = callback_data_parts[-1] == 'True'
    
    print("Callback Data:", callback_query.data)
    print("Selected option index:", selected_option)
    print("Is correct:", is_true)
    
    # Retrieve state data
    data = await state.get_data()
    score = data.get('score', 0)
    current_question_index = data.get('current_question_index', 0)
    questions = data.get('questions', [])

    # Update score if the answer is correct
    if is_true:
        score += 1

    # Move to the next question
    current_question_index += 1

    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        options = [o for o in data.get('options', []) if o['question'] == next_question['id']]
        keyboard = create_inline_keyboard(options)
        await callback_query.message.answer(f"Savol: {next_question['text']}", reply_markup=keyboard)
        await state.update_data(current_question_index=current_question_index, score=score)
    else:
        await callback_query.message.answer(f"Viktorina tugadi. Sizning ballaringiz: {score}")
        await state.clear()

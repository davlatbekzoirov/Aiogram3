from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Abiturient")
        ],
        [
            KeyboardButton(text="Student")
        ]
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

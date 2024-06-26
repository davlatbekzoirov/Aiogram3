from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni"),
            KeyboardButton(text="Reklama yuborish"),
        ],
        [
            KeyboardButton(text='Nomzod')
        ]
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)

plus = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Qo'shish"),
        ],
        [
            KeyboardButton(text='Tugadi')
        ]
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)
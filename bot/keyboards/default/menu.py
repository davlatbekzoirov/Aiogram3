from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Referal link"),
            KeyboardButton(text="Role-ni tanlash"),
        ]
    ],
   resize_keyboard=True,
   input_field_placeholder="Menudan birini tanlang"
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Referal havola"),
        KeyboardButton(text="Mening ballarim"),
    ]
],
    resize_keyboard=True,
    is_persistent=True
)
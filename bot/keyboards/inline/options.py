from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# def create_inline_keyboard(options):
#     keyboard = InlineKeyboardBuilder()
#     for option in options:
#         button = InlineKeyboardButton(text=option["text"], callback_data=f"option_{option['id']}")
#         keyboard.add(button)
#     return keyboard.as_markup()

def create_inline_keyboard(options):
    keyboard = InlineKeyboardBuilder()
    for idx, option in enumerate(options):
        # For demonstration, default to 'False' for is_true. Adjust according to your logic.
        callback_data = f"option_{idx}_False"  # or adjust to include correct data if available
        button = InlineKeyboardButton(text=option, callback_data=callback_data)
        keyboard.add(button)
    return keyboard.as_markup()

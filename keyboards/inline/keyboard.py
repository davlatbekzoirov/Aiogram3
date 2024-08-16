from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='1', callback_data='1')],
        [InlineKeyboardButton(text='2', callback_data='2')],
        [InlineKeyboardButton(text='3', callback_data='3')],
    ]    
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

language = InlineKeyboardMarkup(
	inline_keyboard=[
		[InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="uz")],
		[InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="ru")],
		[InlineKeyboardButton(text="🇺🇸 English", callback_data="en")]
	]
)
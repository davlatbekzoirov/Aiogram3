from aiogram import types, F
from aiogram.filters import CommandStart
from loader import dp, db
from keyboards.inline.language import language
from aiogram.utils.i18n import FSMI18nMiddleware, gettext as _
from utils.schemas.language import LanguageEnum
from aiogram.fsm.context import FSMContext

@dp.message(CommandStart())
async def start_command(message: types.Message, i18n_middleware: FSMI18nMiddleware, state: FSMContext):
    # db.add_user(telegram_id=message.from_user.id, full_name=message.from_user.username)

    await message.answer(_("Assalomu alaykum, {}! Iltimos tilni tanlang").format(message.from_user.full_name))
    await message.answer(_("Здравствуйте, {}! Пожалуйста, выберите язык").format(message.from_user.full_name))
    await message.answer(_("Hello, {}! Please select a language").format(message.from_user.full_name))

    await message.answer(_("Please select your language:"), reply_markup=language)

@dp.callback_query(F.data.in_({"uz", "ru", "en"}))
async def select_language(callback: types.CallbackQuery, state: FSMContext, i18n_middleware: FSMI18nMiddleware):
    selected_language = callback.data
    await callback.answer()  

    await i18n_middleware.set_locale(callback.from_user.id, selected_language)

    if selected_language == "uz":
        await callback.message.answer(_("Siz O'zbek tilini tanladingiz."))
    elif selected_language == "ru":
        await callback.message.answer(_("Вы выбрали русский язык."))
    elif selected_language == "en":
        await callback.message.answer(_("You selected English."))

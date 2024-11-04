from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN
from utils.db_api.sqlite import Database
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database(path_to_db='main.db')
i18n = I18n(path="./languages", domain="messages")
I18n.set_current(i18n)
i18n_middleware = FSMI18nMiddleware(i18n=i18n)
i18n_middleware.setup(dp)
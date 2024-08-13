from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN
from aiogram.enums import ParseMode
# from utils.db_api.api imporsst APIClient

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
# db = APIClient("http://127.0.0.1:8000/api/v1", "davlatbek", "d08980476")
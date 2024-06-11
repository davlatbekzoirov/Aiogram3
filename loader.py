from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN
from aiogram.enums import ParseMode
from utils.db_api.sqlite import Database

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
db = Database(path_to_db='main.db')
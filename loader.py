from aiogram import Bot, Dispatcher
from utils.db_api.db import *
from data.config import BOT_TOKEN
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
db = Database(path_to_db="main.db")
ans = AnswersDatabase(path_to_db="answers.db")
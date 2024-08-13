import time
from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, slow_mode_delay=0.5):
        self.user_timeouts = {}
        self.slow_mode_delay = slow_mode_delay
        super(ThrottlingMiddleware, self).__init__()

    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        current_time = time.time()
        
        # Ushbu foydalanuvchining so'nggi so'rovi bo'yicha yozuv mavjudligini tekshirish
        last_request_time = self.user_timeouts.get(user_id, 0)
        if current_time - last_request_time < self.slow_mode_delay:
            # Agar so'rovlar juda tez-tez bo'lsa, sekin rejimni yoqish
            await event.reply("Juda ko'p so'rov! Biroz kuting.")
            return
        
        else:
            # Oxirgi so'rovning vaqtini yangilash
            self.user_timeouts[user_id] = current_time
            # Event ni handlerga o'tkazish
            return await handler(event, data)
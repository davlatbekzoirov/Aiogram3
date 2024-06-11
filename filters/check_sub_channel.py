from data.config import CHANNELS
from aiogram import filters,Bot
from aiogram.types import Message


class IsCheckSubChannels(filters.Filter):

    async def __call__(self,message:Message,bot:Bot):
        if not CHANNELS:
            return False
        
        for channel in CHANNELS:
            result = await bot.get_chat_member(channel,message.from_user.id)
            if result.status in ["member","adminstrator","creator"]:
                return False
        return True
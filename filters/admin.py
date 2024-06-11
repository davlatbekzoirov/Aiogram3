from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsBotAdminFilter(BaseFilter):
    def __init__(self, user_ids: list):
        self.user_ids = user_ids

    async def __call__(self, message: Message) -> bool:
        # Berilgan foydalanuvchi ID larini integer (butun son) qilib olamiz
        admin_ids_int = [int(id) for id in self.user_ids]
        # Xabarda yuboruvchi foydalanuvchi ID sini integer qilib olamiz
        sender_id = int(message.from_user.id)
        # Agar foydalanuvchi ID si bot administratorlari ID laridan biriga teng bo'lsa
        # True qaytaradi, aks holda False qaytaradi
        return sender_id in admin_ids_int

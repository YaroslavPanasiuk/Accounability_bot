# filters/is_admin.py
from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.config import config
from bot.lexicon import Lexicon

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == config.ADMIN_ID:
            return True
        return False

class IsMentor(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == config.MENTOR_ID:
            return True
        return False

class IsDisciple(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id == config.DISCIPLE_ID:
            return True
        return False
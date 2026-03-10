from aiogram import Dispatcher
from . import common, mentor, disciple

def register_handlers(dp: Dispatcher):
    dp.include_router(mentor.router)
    dp.include_router(disciple.router)
    dp.include_router(common.router)
from aiogram import Dispatcher
from . import common

def register_handlers(dp: Dispatcher):
    dp.include_router(common.router)
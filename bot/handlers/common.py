from bot.utils.formatters import random_bible_verse
from bot.config import Config
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta
from bot.utils.keyboards import *
from bot.lexicon import Lexicon
from bot.utils.handle_json import *

class StatisticsCollection(StatesGroup):
    waiting_for_answer = State()

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = get_disciple_main_menu_keyboard()
    await message.answer(Lexicon.DEFAULT_MESSAGE, reply_markup=kb)

@router.message()
async def default_handler(message: types.Message):
    await message.answer(random_bible_verse())
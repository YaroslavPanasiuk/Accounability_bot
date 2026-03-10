from email import message

from bot.config import Config
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.state import StatesGroup, State
from babel.dates import format_date
from bot.utils.formatters import format_daily_stats
from datetime import datetime, timedelta
from bot.utils.keyboards import *
from bot.filters.by_id import IsMentor
from bot.lexicon import Lexicon, LexiconFilter
from bot.utils.handle_json import *
from aiogram.fsm.context import FSMContext

class MentorStatisticsCollection(StatesGroup):
    waiting_for_answer = State()
    waiting_for_day = State()

router = Router()
router.message.filter(IsMentor())

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = get_mentor_main_menu_keyboard()
    await message.answer(Lexicon.MENTOR_START_MESSAGE, reply_markup=kb)

@router.message(or_f(Command("show_stats"),LexiconFilter("SHOW_STATS_CMD")))
async def show_stats(message: types.Message):
    stats = get_stats_from_json(datetime.now() - timedelta(hours=Config.TRESHOLD_HOURS))
    await message.answer(
        format_daily_stats(datetime.now() - timedelta(hours=Config.TRESHOLD_HOURS), stats),
        reply_markup=get_mentor_main_menu_keyboard(), parse_mode="MarkdownV2"
    )

@router.message(or_f(Command("show_old_stats"),LexiconFilter("SHOW_PREVIOUS_STATS_CMD")))
async def cmd_fill_previous_stats(message: types.Message, state: FSMContext):
    dates = get_date_list()
    dates.reverse()
    if not dates:
        await message.answer(Lexicon.NO_STATS_AVAILABLE)
        return
    keyboard = get_previous_days_keyboard(dates)
    await state.set_state(MentorStatisticsCollection.waiting_for_day)
    await message.answer(Lexicon.SELECT_PREVIOUS_DAY, reply_markup=keyboard)

@router.callback_query(MentorStatisticsCollection.waiting_for_day, F.data.startswith("page_"))
async def set_page(callback: types.CallbackQuery):
    dates = get_date_list()
    dates.reverse()
    data = callback.data 
    new_page = int(data.split("_")[1])
    new_kb = get_previous_days_keyboard(dates, page=new_page)
    await callback.message.edit_text(callback.message.text, reply_markup=new_kb)
    await callback.answer()

@router.callback_query(MentorStatisticsCollection.waiting_for_day, F.data.startswith("item_"))
async def fill_stats_for_selected_day(callback: types.CallbackQuery):
    data = callback.data 
    date = datetime.strptime(data.split("_")[1].split(" - ")[0], "%d.%m.%Y")
    stats = get_stats_from_json(date)
    await callback.message.edit_text(format_daily_stats(date, stats), parse_mode="MarkdownV2")
    await callback.message.edit_reply_markup(get_mentor_main_menu_keyboard())
    await callback.answer()